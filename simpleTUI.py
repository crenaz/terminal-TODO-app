import rich.box
from rich.panel import Panel
from textual.app import App
from textual.widgets import Footer, Header, Static
from textual_inputs import TextInput

class SimpleForm(App):
    def __init__(self, *args) -> None:
        super().__init__(*args)

    async def on_load(self) -> None:
        # Bind the q button to quit.
        await self.bind("q", "quit", "Quit")

        # Bind the enter key to the action_submit function.
        await self.bind("enter", "submit", "Submit")

    async def on_mount(self) -> None:
        # Placing Header and Footer at the top and bottom
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")

        # Creates a Text Input that allows you to type text
        self.text = TextInput(
            name="Text",
            placeholder="enter your Text...",
            title="Text",
        )

        # Creates a Panel that displays your text.
        self.output = Static(
            renderable=Panel(
                "", title="Output", border_style="blue", box=rich.box.SQUARE
            )
        )

        # Defining the Placement for the output panel and text.
        await self.view.dock(self.output, edge="left", size=40)
        await self.view.dock(self.text, edge="top")

    async def action_submit(self) -> None:
        # Retrieve the value from the Input text box.
        val = self.text.value

        # Format and update the value in the output panel
        await self.output.update(
            Panel(val, title="Output", border_style="blue", box=rich.box.SQUARE)
        )

        # Empty the text box for the next input.
        self.text.value = ""

# Running our form here...
if __name__ == "__main__":
    SimpleForm.run(title='Simple TUI', log="textual.log")
