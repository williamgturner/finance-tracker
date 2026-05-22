import os
from textual import on
from textual.events import Mount
from dotenv import load_dotenv

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Static, SelectionList, Footer

from graph_view import GraphView
from apihandler import ApiHandler


class FinanceApp(App):

    def compose(self) -> ComposeResult:
        yield GraphView()
        yield SelectionList()

    @on(SelectionList.SelectedChanged)
    async def update_selected_view(self) -> None:
        net_balance_series = await self.api.getAccountTransactions(self.query_one(SelectionList).selected)
        self.query_one(GraphView).data=net_balance_series

    async def on_mount(self) -> None:
        load_dotenv()
        self.api = ApiHandler(
            os.getenv("TOKEN"),
            os.getenv("APP_TOKEN")
        )
        accountList=self.query_one(SelectionList)
        for account in await self.api.getAccountList():
            accountList.add_option((account[0], account[1]))



if __name__ == "__main__":
    FinanceApp().run()