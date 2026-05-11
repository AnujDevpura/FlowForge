export type Dependency = {
    task_id: string
    depends_on_task_id: string
}

export type Execution = {
    id: string

    attempt_number: number

    status: string

    logs: string | null

    worker_id: string | null

    started_at: string | null

    completed_at: string | null

    error_message: string | null
}

export type Task = {
    id: string

    name: string

    status: string

    retry_count: number

    max_retries: number

    started_at: string | null

    completed_at: string | null

    last_error: string | null

    executions: Execution[]
}

export type Job = {
    id: string

    name: string

    status: string

    created_at: string

    updated_at: string

    tasks: Task[]

    dependencies: Dependency[]
}