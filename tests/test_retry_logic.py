from services.task_execution import (
    calculate_retry_delay,
)


def test_exponential_backoff_values():

    assert (
        calculate_retry_delay(1)
        == 2
    )

    assert (
        calculate_retry_delay(2)
        == 4
    )

    assert (
        calculate_retry_delay(3)
        == 8
    )