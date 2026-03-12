import json
from pathlib import Path

import rich.box
from rich.panel import Panel
from textual.app import App
from textual.widgets import Footer, Header, Static
from textual_inputs import TextInput


class SimpleForm(App):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.storage_path = Path("tasks.json")
        self.tasks = []
        self.status_message = "Type 'add <task>', 'done <n>', or 'del <n>'."
        self._load_tasks()

    def _load_tasks(self) -> None:
        """Load tasks from disk if a save file exists."""
        try:
            if self.storage_path.exists():
                data = json.loads(self.storage_path.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    # Basic validation: each item should be a dict with title/done.
                    cleaned = []
                    for item in data:
                        if (
                            isinstance(item, dict)
                            and "title" in item
                            and "done" in item
                        ):
                            cleaned.append(
                                {"title": str(item["title"]), "done": bool(item["done"])}
                            )
                    self.tasks = cleaned
                    if self.tasks:
                        self.status_message = "Loaded tasks from tasks.json."
        except Exception:
            # Ignore corrupt files; start with an empty list.
            self.tasks = []

    def _save_tasks(self) -> None:
        """Persist tasks to disk."""
        try:
            self.storage_path.write_text(
                json.dumps(self.tasks, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception:
            # If saving fails, don't crash the UI; leave status as-is.
            pass

    async def on_load(self) -> None:
        # Bind the q button to quit.
        await self.bind("q", "quit", "Quit")

        # Bind the enter key to the action_submit function.
        await self.bind("enter", "submit", "Submit")

    async def on_mount(self) -> None:
        # Placing Header and Footer at the top and bottom
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")

        # Creates a Text Input that allows you to type commands
        self.text = TextInput(
            name="Text",
            placeholder="add <task>, done <n>, del <n>",
            title="TODO Input",
        )

        # Creates a Panel that displays your TODO list.
        self.output = Static(
            renderable=Panel(
                "", title="TODOs", border_style="blue", box=rich.box.SQUARE
            )
        )

        # Defining the Placement for the output panel and text.
        await self.view.dock(self.output, edge="left", size=40)
        await self.view.dock(self.text, edge="top")

        await self.refresh_output()

    def _build_panel(self) -> Panel:
        """Build the panel showing current tasks and help."""
        if not self.tasks:
            body_lines = ["No tasks yet.", "Use 'add <task>' to create one."]
        else:
            body_lines = []
            for index, task in enumerate(self.tasks, start=1):
                status = "[green][x][/green]" if task["done"] else "[red][ ][/red]"
                body_lines.append(f"{index}. {status} {task['title']}")

        body_lines.append("")
        body_lines.append(self.status_message)

        body = "\n".join(body_lines)
        return Panel(body, title="TODOs", border_style="blue", box=rich.box.SQUARE)

    async def refresh_output(self) -> None:
        """Re-render the TODO list panel."""
        await self.output.update(self._build_panel())

    async def action_submit(self) -> None:
        raw = self.text.value.strip()
        # Empty the text box for the next input.
        self.text.value = ""

        if not raw:
            self.status_message = "Empty input ignored. Use 'add <task>'."
            await self.refresh_output()
            return

        parts = raw.split(maxsplit=1)
        command = parts[0].lower()
        argument = parts[1] if len(parts) > 1 else ""

        if command in ("add", "a"):
            title = argument.strip()
            if not title:
                self.status_message = "Cannot add an empty task."
            else:
                self.tasks.append({"title": title, "done": False})
                self.status_message = f"Added task: {title!r}"
        elif command in ("done", "d"):
            if not argument.isdigit():
                self.status_message = "Usage: done <task_number>"
            else:
                index = int(argument) - 1
                if 0 <= index < len(self.tasks):
                    self.tasks[index]["done"] = True
                    self.status_message = f"Marked task {argument} as done."
                else:
                    self.status_message = f"No task with number {argument}."
        elif command in ("undone", "u"):
            if not argument.isdigit():
                self.status_message = "Usage: undone <task_number>"
            else:
                index = int(argument) - 1
                if 0 <= index < len(self.tasks):
                    self.tasks[index]["done"] = False
                    self.status_message = f"Marked task {argument} as not done."
                else:
                    self.status_message = f"No task with number {argument}."
        elif command in ("del", "delete", "remove", "rm"):
            if not argument.isdigit():
                self.status_message = "Usage: del <task_number>"
            else:
                index = int(argument) - 1
                if 0 <= index < len(self.tasks):
                    removed = self.tasks.pop(index)
                    self.status_message = (
                        f"Deleted task {argument}: {removed['title']!r}"
                    )
                else:
                    self.status_message = f"No task with number {argument}."
        else:
            # Treat unrecognized input as a shorthand for adding a task.
            self.tasks.append({"title": raw, "done": False})
            self.status_message = f"Added task: {raw!r}"

        self._save_tasks()
        await self.refresh_output()

# Running our form here...
if __name__ == "__main__":
    SimpleForm.run(title='Simple TUI', log="textual.log")
