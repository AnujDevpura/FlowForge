from collections import defaultdict

from schemas.job import JobCreate

def validate_dag(job_data: JobCreate) -> None:
    task_names = set()

    for task in job_data.tasks:

        if task.name in task_names:
            raise ValueError(
                f"Duplicate task name: {task.name}"
            )

        task_names.add(task.name)

    graph = defaultdict(list)

    for task in job_data.tasks:

        for dependency in task.dependencies:

            if dependency not in task_names:
                raise ValueError(
                    f"Task '{task.name}' depends on unknown task '{dependency}'"
                )

            if dependency == task.name:
                raise ValueError(
                    f"Task '{task.name}' cannot depend on itself"
                )

            graph[dependency].append(task.name)

    visited = set()

    visiting = set()

    def dfs(node: str):

        if node in visiting:
            raise ValueError(
                "Cycle detected in DAG"
            )

        if node in visited:
            return

        visiting.add(node)

        for neighbor in graph[node]:
            dfs(neighbor)

        visiting.remove(node)

        visited.add(node)

    for task_name in task_names:
        dfs(task_name)