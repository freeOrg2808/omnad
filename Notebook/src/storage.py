import json
from pathlib import Path
from src.NoteBase import NoteBase


class JSONStorage:
    def __init__(self, file_path="src/notes.json"):
        self.file_path = Path(file_path)

    def load_all(self) -> dict:
        if not self.file_path.exists():
            return {}

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            return {}

        notes_dict = {}
        for str_id, note_data in data.items():
            notes_dict[int(str_id)] = NoteBase.from_dict(note_data)

        return notes_dict

    def save_all(self, notes_dict: dict):
        data_to_save = {}
        for note_id, note_obj in notes_dict.items():
            data_to_save[str(note_id)] = note_obj.to_dict()

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)

    def add_note(self, note_obj):
        notes = self.load_all()
        notes[note_obj.note_id] = note_obj
        self.save_all(notes)

    def get_note(self, note_id: int):
        notes = self.load_all()
        return notes.get(note_id)

    def delete_note(self, note_id: int) -> bool:
        notes = self.load_all()
        if note_id in notes:
            del notes[note_id]
            self.save_all(notes)
            return True
        return False