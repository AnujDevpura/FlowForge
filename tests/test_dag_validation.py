import pytest

from utils.dag_validation import validate_dag
from schemas.job import JobCreate

def test_valid_dag_passes():

    tasks = [
        {
            "name": "task_a",

            "payload": {
                "type": "print",
                "message": "A",
            },
        },
        {
            "name": "task_b",

            "payload": {
                "type": "print",
                "message": "B",
            },

            "dependencies": [
                "task_a",
            ],
        },
    ]


def test_cycle_detection_raises_error():

    tasks = [
        {
            "name": "task_a",

            "payload": {
                "type": "print",
                "message": "A",
            },

            "dependencies": [
                "task_b",
            ],
        },
        {
            "name": "task_b",

            "payload": {
                "type": "print",
                "message": "B",
            },

            "dependencies": [
                "task_a",
            ],
        },
    ]

    with pytest.raises(ValueError):

        validate_dag(
            JobCreate(
                name="test_job",
                tasks=tasks,
            )
        )