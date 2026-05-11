from datetime import datetime


def append_log(
    execution,
    message: str,
):

    timestamp = (
        datetime.utcnow()
        .strftime("%H:%M:%S")
    )

    new_line = (
        f"[{timestamp}] {message}"
    )

    if execution.logs:

        execution.logs += (
            "\n" + new_line
        )

    else:

        execution.logs = new_line