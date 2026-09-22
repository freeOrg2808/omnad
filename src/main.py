import typer

from src.cli.notes import app as notes_app

app = typer.Typer(help="Notebook CLI - Your personal terminal notebook")

app.add_typer(notes_app, name="note", help="Manage your notes (add, list, delete, etc.)")

if __name__ == "__main__":
    app()