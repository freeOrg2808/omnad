import typer
from src.storage import JSONStorage
from typing_extensions import Annotated
from typing import List
from datetime import datetime
from rich.console import Console
from rich.table import Table
from src.NoteBase import NoteSimple, NoteBookmark, NoteList
from rich.panel import Panel

app = typer.Typer(help="Notebook CLI - Manage your notes from the terminal.")
storage = JSONStorage()
console = Console()


@app.command(name="add")
def add_note(
        title: str = typer.Argument(..., help="The title of the new note"),
        content: str = typer.Option("", "-m", "--message", help="Inline content for the note"),
        url: str = typer.Option(None, "-u", "--url", help="Create a bookmark note with a URL")
):
    notes_dict = storage.load_all()
    new_id = max(notes_dict.keys()) + 1 if notes_dict else 1
    now = datetime.now()
    if url:
        new_note = NoteBookmark(content=url, note_id=new_id, title=title, createdAt=now, updatedAt=now)
        note_type_str = "Bookmark"
    else:
        final_content = content if content else "No content provided."
        new_note = NoteSimple(content=final_content, note_id=new_id, title=title, createdAt=now, updatedAt=now)
        note_type_str = "Note"
    storage.add_note(new_note)
    console.print(f"[bold green]Success![/bold green] {note_type_str} '{title}' created with ID: [cyan]{new_id}[/cyan]")


@app.command(name="list")
def add_list_note(
        title: str = typer.Argument(..., help="The title of the new list note"),
        items: List[str] = typer.Option(..., "-i", "--item", help="Items for the list (can be used multiple times)")
):
    notes_dict = storage.load_all()
    new_id = max(notes_dict.keys()) + 1 if notes_dict else 1
    now = datetime.now()

    new_note = NoteList(content=items, note_id=new_id, title=title, createdAt=now, updatedAt=now)

    storage.add_note(new_note)
    console.print(f"[bold green]Success![/bold green] List '{title}' created with ID: [cyan]{new_id}[/cyan]")


@app.command(name="all")
def list_all_notes():
    notes_dict = storage.load_all()
    if not notes_dict:
        console.print("[yellow]No notes found. Time to create some![/yellow]")
        return
    table = Table(title="My Notes")
    table.add_column("ID", style="cyan", justify="left")
    table.add_column("Type", style="blue")
    table.add_column("Title", style="magenta")
    table.add_column("Date", style="dim")
    for note_id, note_obj in notes_dict.items():
        note_type = note_obj.__class__.__name__.replace("Note", "")
        date_str = note_obj.createdAt.strftime("%Y-%m-%d %H:%M")
        table.add_row(
            str(note_obj.note_id),
            note_type,
            note_obj.title,
            date_str
        )
    console.print(table)


@app.command(name="delete")
def delete_note(
        note_id: Annotated[int, typer.Argument(help="The ID of the note to delete")],
        force: Annotated[bool, typer.Option("-f", "--force", help="Skip confirmation prompt")] = False
):
    note = storage.get_note(note_id)
    if not note:
        console.print(f"[bold red]Error:[/bold red] Note with ID '{note_id}' not found.")
        raise typer.Exit(code=1)
    if not force:
        confirm = typer.confirm(f"Are you sure you want to delete '{note.title}'?")
        if not confirm:
            console.print("[yellow]Deletion cancelled.[/yellow]")
            raise typer.Abort()
    success = storage.delete_note(note_id)
    if success:
        console.print(f"[bold green]Deleted:[/bold green] Note '{note_id}' has been removed.")


@app.command(name="read")
def read_note(
        note_id: int = typer.Argument(..., help="The ID of the note to read")
):
    note = storage.get_note(note_id)
    if note:
        console.print(f"\n[bold magenta]🏷️ {note.title}[/bold magenta] (ID: {note.note_id})")
        console.print(f"[dim]Created: {note.createdAt.strftime('%Y-%m-%d %H:%M')}[/dim]\n")
        if isinstance(note, NoteBookmark):
            console.print(f"🔗 [blue]Opening Bookmark URL:[/blue] {note.content}")
            note.openUrl()
        elif isinstance(note, NoteSimple):
            console.print(Panel(note.content, border_style="green", expand=False))
        elif isinstance(note, NoteList):
            for item in note.content:
                console.print(f"  • {item}")
        else:
            console.print(note)
        console.print()
        return
    console.print(f"[bold red]Error:[/bold red] Note with ID '{note_id}' not found.")
    raise typer.Exit(code=1)
