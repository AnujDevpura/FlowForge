import httpx

from executors.base import BaseExecutor


class HTTPExecutor(BaseExecutor):

    async def execute(
        self,
        payload: dict,
        context,
    ):

        url = payload["url"]

        async with httpx.AsyncClient() as client:

            response = await client.get(url)

            print(
                f"[HTTP EXECUTOR] "
                f"{url} -> "
                f"{response.status_code}"
            )

            print(
                f"[HTTP EXECUTOR] "
                f"Dependency context: {context}"
            )

            try:

                data = response.json()

            except Exception:

                data = response.text

            summarized_response = self.build_summary(
                data
            )

            return {
                "url": url,
                "status_code": response.status_code,
                "summary": summarized_response,
            }

    def build_summary(
        self,
        data,
    ):

        if isinstance(data, list):

            return {
                "type": "list",
                "items_count": len(data),
                "sample": data[:3],
            }

        if isinstance(data, dict):

            return {
                "type": "object",
                "keys": list(data.keys()),
                "sample": {
                    key: data[key]
                    for key in list(data.keys())[:5]
                },
            }

        text = str(data)

        return {
            "type": "text",
            "preview": text[:500],
        }