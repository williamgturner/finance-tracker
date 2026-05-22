# apihandler.py

import httpx
from collections import defaultdict
from datetime import datetime

class ApiHandler:

    def __init__(self, token: str, appToken: str):

        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {token}",
                "X-Akahu-Id": appToken,
                "Content-Type": "application/json"
            },
            timeout=30.0
        )

    async def getAccountList(self):
        accounts = []

        response = await self.client.get(
            "https://api.akahu.io/v1/accounts"
        )

        # Debugging output
        print("STATUS:", response.status_code)
        print("BODY:", response.text)

        response.raise_for_status()
        data=response.json()
        items = data.get("items", [])
        for account in items:
                name = account.get("name", "Unnamed Account")
                acc_id = account.get("_id", "")
                balance = account.get("balance", 0).get("current")
                accounts.append((name, acc_id, balance))
    
        return accounts

    async def getAccountTransactions(self, acc_ids, start=None, end=None):
        """
        Returns: [(date, net_balance), ...] aggregated across all accounts
        """

        if isinstance(acc_ids, str):
            acc_ids = [acc_ids]

        all_transactions = []

        # Fetch all accounts
        for acc_id in acc_ids:

            cursor = None

            while True:
                params = {}
                if cursor:
                    params["cursor"] = cursor
                if start:
                    params["start"] = start
                if end:
                    params["end"] = end
                response = await self.client.get(
                    f"https://api.akahu.io/v1/accounts/{acc_id}/transactions",
                    params=params
                )
                response.raise_for_status()
                data = response.json()

                items = data.get("items", [])
                all_transactions.extend(items)

                cursor = data.get("cursor", {}).get("next")

                if not cursor:
                    break

        # Normalise dates
        for tx in all_transactions:
            tx["_day"] = datetime.fromisoformat(tx["date"]).date()

        all_transactions.sort(key=lambda x: x["date"])

        # Daily net
        daily_delta = defaultdict(float)

        for tx in all_transactions:
            daily_delta[tx["_day"]] += tx["amount"]

        # Cumulative balance
        balance_series = []
        running_balance = 0.0

        for day in sorted(daily_delta.keys()):
            running_balance += daily_delta[day]
            formatted_day = day.strftime("%d/%m/%Y")
            balance_series.append((formatted_day, running_balance))

        return balance_series

    async def close(self):
        await self.client.aclose()