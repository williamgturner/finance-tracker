# apihandler.py

import httpx


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

        response = await self.client.get(
            "https://api.akahu.io/v1/accounts"
        )

        # Debugging output
        print("STATUS:", response.status_code)
        print("BODY:", response.text)

        response.raise_for_status()

        return response.json()

    async def close(self):
        await self.client.aclose()