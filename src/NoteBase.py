from datetime import datetime
import webbrowser
from rich.console import Console
from rich.panel import Panel


class NoteBase:
    def __init__(self, note_id: int, title: str, createdAt: datetime, updatedAt: datetime):
        self.note_id = note_id
        self.title = title
        self.createdAt = createdAt
        self.updatedAt = updatedAt

    def to_dict(self) -> dict:
        return {
            "_type": self.__class__.__name__,
            "note_id": self.note_id,
            "title": self.title,
            "createdAt": self.createdAt.isoformat(),
            "updatedAt": self.updatedAt.isoformat(),
        }

    @staticmethod
    def from_dict(data: dict):
        created = datetime.fromisoformat(data["createdAt"])
        updated = datetime.fromisoformat(data["updatedAt"])
        note_type = data.get("_type")

        factory_registry = {
            "NoteSimple": NoteSimple,
            "NoteList": NoteList,
            "NoteBookmark": NoteBookmark
        }

        note_class = factory_registry.get(note_type)
        if not note_class:
            raise ValueError(f"Unknown note type: {note_type}")

        content_data = data.get("content", data.get("contents"))

        return note_class(content=content_data, note_id=data["note_id"], title=data["title"], createdAt=created,
                          updatedAt=updated)

    def display(self, console: Console):
        pass

    def __str__(self):
        return f"{self.note_id}, {self.title}"


class NoteSimple(NoteBase):
    def __init__(self, content: str, note_id: int, title: str, createdAt: datetime, updatedAt: datetime):
        super().__init__(note_id, title, createdAt, updatedAt)
        self.content = content

    def to_dict(self):
        data = super().to_dict()
        data["content"] = self.content
        return data

    def display(self, console: Console):
        console.print(Panel(self.content, border_style="green", expand=False))

    def __str__(self):
        return f"{self.note_id}, {self.title}, {self.content}"


class NoteList(NoteBase):
    def __init__(self, content: list[str], note_id: int, title: str, createdAt: datetime, updatedAt: datetime):
        super().__init__(note_id, title, createdAt, updatedAt)
        self.contents = content

    def to_dict(self):
        data = super().to_dict()
        data["contents"] = self.contents
        return data

    def display(self, console: Console):
        for item in self.contents:
            console.print(f"  • {item}")

    def __str__(self):
        return f"{self.note_id}, {self.title}, {self.contents}"


class NoteBookmark(NoteBase):
    def __init__(self, content: str, note_id: int, title: str, createdAt: datetime, updatedAt: datetime):
        super().__init__(note_id, title, createdAt, updatedAt)
        self.content = content

    def to_dict(self):
        data = super().to_dict()
        data["content"] = self.content
        return data

    def openUrl(self):
        webbrowser.open(self.content)

    def display(self, console: Console):
        console.print(f"🔗 [blue]Opening Bookmark URL:[/blue] {self.content}")
        self.openUrl()

    def __str__(self):
        return f"{self.note_id}, {self.title}, {self.content}"
