from executors.base import BaseExecutor

from utils.execution_logs import (
    append_log,
)


class PrintExecutor(BaseExecutor):

    async def execute(
        self,
        payload: dict,
        context,
        execution=None,
    ):

        message = payload.get(
            "message",
            ""
        )

        if execution:

            append_log(
                execution,
                f"Printing message: {message}",
            )

        print(
            f"PRINT TASK: {message}"
        )

        print(
            f"CONTEXT: {context}"
        )

        if execution:

            append_log(
                execution,
                "Print task completed",
            )

        return {
            "printed_message":
                message,

            "context_received":
                True,
        }