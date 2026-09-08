from datetime import datetime
import webbrowser

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

        if note_type == "NoteSimple":
            return NoteSimple(data["content"], data["note_id"], data["title"], created, updated)
        elif note_type == "NoteList":
            return NoteList(data["content"], data["note_id"], data["title"], created, updated)
        elif note_type == "NoteBookmark":
            return NoteBookmark(data["content"], data["note_id"], data["title"], created, updated)
        else:
            raise ValueError(f"Unknown note type: {note_type}")

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

    def __str__(self):
        return f"{self.note_id}, {self.title}, {self.content}"


class NoteList(NoteBase):
    def __init__(self, content: list[str], note_id: int, title: str, createdAt: datetime, updatedAt: datetime):
        super().__init__(note_id, title, createdAt, updatedAt)
        self.content = content

    def to_dict(self):
        data = super().to_dict()
        data["content"] = self.content
        return data

    def __str__(self):
        return f"{self.note_id}, {self.title}, {self.content}"


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

    def __str__(self):
        return f"{self.note_id}, {self.title}, {self.content}"