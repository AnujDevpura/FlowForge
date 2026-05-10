import httpx

from executors.base import BaseExecutor


class HTTPExecutor(BaseExecutor):

    async def execute(
        self,
        payload: dict,
    ):

        url = payload["url"]

        async with httpx.AsyncClient() as client:

            response = await client.get(url)

            print(
                f"[HTTP EXECUTOR] {url} -> {response.status_code}"
            )