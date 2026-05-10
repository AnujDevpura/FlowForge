from executors.base import BaseExecutor


class PrintExecutor(BaseExecutor):

    async def execute(
        self,
        payload: dict,
    ):

        message = payload.get(
            "message",
            ""
        )

        print(
            f"[PRINT EXECUTOR]: {message}"
        )