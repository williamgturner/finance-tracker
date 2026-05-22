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

        # 🔥 initial test graph data
        graph = self.query_one(GraphView)
        graph.data = [
            ("9/06/2025", 1),
            ("9/06/2025", 3),
            ("9/06/2025", 2),
        ]

    def on_selection_list_selection_changed(
        self,
        event: SelectionList.SelectionChanged
    ) -> None:

        output = self.query_one("#output", Static)
        output.update(f"Selected: {event.selection}")

        graph = self.query_one(GraphView)

        value = len(event.selection) if event.selection else 0

        graph.data = [
            ("29/06/2025", value),
            ("29/08/2025", value + 2),
            ("29/07/2025", value + 1),
        ]

    async def on_unmount(self) -> None:
        if hasattr(self, "api"):
            await self.api.close()
