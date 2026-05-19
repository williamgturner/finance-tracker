from textual.app import App, ComposeResult, RenderResult
from textual.widget import Widget
from textual.widgets import Label, Input


class GraphView(Widget):

    def __init__(self, input_label: str) -> None:
        self.input_label = input_label
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label(self.input_label)
        yield Input()
