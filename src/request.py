import os
from dotenv import load_dotenv

from textual.app import App, ComposeResult
from textual.widgets import Static, SelectionList

from apihandler import ApiHandler


class FinanceApp(App):

    def compose(self) -> ComposeResult:
        yield SelectionList[str](id="accounts")
        yield Static("Loading accounts...", id="output")

    async def on_mount(self) -> None:

        load_dotenv()

        self.api = ApiHandler(
            os.getenv("TOKEN"),
            os.getenv("APP_TOKEN")
        )

        output = self.query_one("#output", Static)
        account_list = self.query_one("#accounts", SelectionList)

        try:
            accounts = await self.api.getAccountList()
            items = accounts.get("items", [])

            account_list.clear_options()

            for account in items:
                name = account.get("name", "Unnamed Account")
                acc_id = account.get("_id", "")

                account_list.add_option((name, acc_id))

            output.update(f"Loaded {len(items)} accounts")

        except Exception as e:
            output.update(f"ERROR:\n{e}")

    def on_selection_list_selection_changed(self, event: SelectionList.SelectionChanged) -> None:
        output = self.query_one("#output", Static)
        output.update(f"Selected: {event.selection}")

    async def on_unmount(self) -> None:
        await self.api.close()


if __name__ == "__main__":
    FinanceApp().run()