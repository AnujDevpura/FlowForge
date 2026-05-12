import {
    useEffect,
    useState,
} from "react"

import {
    useParams,
} from "react-router-dom"

import {
    ChevronDown,
    ChevronRight,
} from "lucide-react"

import {
    fetchJobDetails,
} from "../api/jobDetails"

import WorkflowGraph from "../components/WorkflowGraph"
import StatusBadge from "../components/StatusBadge"
import RetryDots from "../components/RetryDots"

import {
    formatTimestamp,
} from "../components/time"

import type {
    Job,
    Task,
} from "../types/job"



function getDuration(
    startedAt: string | null,
    completedAt: string | null,
) {

    if (
        !startedAt
        ||
        !completedAt
    ) {
        return null
    }

    const start =
        new Date(startedAt)

    const end =
        new Date(completedAt)

    const seconds =
        (
            end.getTime()
            -
            start.getTime()
        ) / 1000

    return seconds.toFixed(2)
}


function JobDetailsPage() {

    const { jobId } =
        useParams()

    const [job, setJob] =
        useState<Job | null>(null)

    const [
        expandedExecutions,
        setExpandedExecutions,
    ] = useState<
        Record<string, boolean>
    >({})


    function toggleExecution(
        executionId: string,
    ) {

        setExpandedExecutions(
            (prev) => ({
                ...prev,

                [executionId]:
                    !prev[executionId],
            })
        )
    }


    useEffect(() => {

        async function loadJob() {

            if (!jobId) {
                return
            }

            try {

                const data =
                    await fetchJobDetails(
                        jobId
                    )

                setJob(data)

            } catch (error) {

                console.error(error)
            }
        }

        loadJob()

        const interval = setInterval(
            loadJob,
            3000,
        )

        return () => clearInterval(
            interval
        )

    }, [jobId])


    if (!job) {

        return (
            <div>
                Loading...
            </div>
        )
    }


    function isBlockedTask(
    task: Task,
    visited = new Set<string>(),
): boolean {

    if (!job) {
        return false
    }

    if (
        task.status !== "PENDING"
    ) {
        return false
    }

    if (
        visited.has(task.id)
    ) {
        return false
    }

    visited.add(task.id)

    const dependencyIds =
        job.dependencies
            .filter(
                (dep) =>
                    dep.task_id === task.id
            )
            .map(
                (dep) =>
                    dep.depends_on_task_id
            )

    const dependencyTasks =
        job.tasks.filter(
            (t) =>
                dependencyIds.includes(
                    t.id
                )
        )

    return dependencyTasks.some(
        (dependencyTask) =>

            dependencyTask.status
            ===
            "FAILED"

            ||

            isBlockedTask(
                dependencyTask,
                visited,
            )
    )
}


    return (
        <div className="mx-auto max-w-7xl">

            <div className="mb-8">

                <h1 className="text-4xl font-black tracking-tight mb-3">
                    {job.name}
                </h1>

                <StatusBadge
                    status={job.status}
                />

                <div className="text-zinc-500 mt-3">

                    Created:
                    {" "}

                    {formatTimestamp(
                        job.created_at
                    )}

                </div>

            </div>


            <div className="mb-8">

                <h2 className="text-2xl font-bold mb-4">
                    Workflow Graph
                </h2>

                <WorkflowGraph
                    tasks={job.tasks}
                    dependencies={job.dependencies}
                    isBlockedTask={isBlockedTask}
                />

            </div>


            <div>

                <h2 className="text-2xl font-bold mb-4">
                    Tasks
                </h2>

                <div className="space-y-6">

                    {job.tasks.map((task) => (

                        <div
                            key={task.id}
                            className="
                                border border-zinc-800/90 rounded-2xl p-5
                                bg-gradient-to-b from-zinc-900/90 to-zinc-950/90
                            "
                        >

                            <div
                                className="
                                    flex
                                    items-center
                                    justify-between
                                    mb-3
                                "
                            >

                                <div className="text-xl font-semibold">

                                    {task.name}

                                </div>

                                <StatusBadge
                                    status={
                                        isBlockedTask(task)
                                            ? "BLOCKED"
                                            : task.status
                                    }
                                />

                            </div>


                            {getDuration(
                                task.started_at,
                                task.completed_at,
                            ) && (

                                <div className="text-zinc-500 text-sm">

                                    Duration:
                                    {" "}

                                    {getDuration(
                                        task.started_at,
                                        task.completed_at,
                                    )}

                                    s

                                </div>
                            )}


                            <div className="text-zinc-500 text-sm mt-2">

                                Retries:
                                {" "}

                                {task.retry_count}
                                /
                                {task.max_retries}

                                <RetryDots
                                    retryCount={
                                        task.retry_count
                                    }
                                    maxRetries={
                                        task.max_retries
                                    }
                                    status={
                                        task.status
                                    }
                                />

                            </div>


                            {task.executions.length > 0 && (

                                <div className="mt-6">

                                    <h3
                                        className="
                                            text-sm
                                            font-semibold
                                            mb-3
                                            text-zinc-400
                                        "
                                    >
                                        Execution History
                                    </h3>

                                    <div className="space-y-3">

                                        {task.executions.map(
                                            (execution) => (

                                                <div
                                                    key={
                                                        execution.id
                                                    }
                                                    className="
                                                        border border-zinc-800
                                                        rounded-xl p-3
                                                        bg-zinc-950/80
                                                    "
                                                >

                                                    <button
                                                        onClick={() =>
                                                            toggleExecution(
                                                                execution.id
                                                            )
                                                        }
                                                        className="
                                                            w-full
                                                            flex
                                                            items-center
                                                            justify-between
                                                        "
                                                    >

                                                        <div
                                                            className="
                                                                flex
                                                                items-center
                                                                gap-3
                                                            "
                                                        >

                                                            {
                                                                expandedExecutions[
                                                                    execution.id
                                                                ]
                                                                    ? (
                                                                        <ChevronDown
                                                                            size={
                                                                                16
                                                                            }
                                                                        />
                                                                    )
                                                                    : (
                                                                        <ChevronRight
                                                                            size={
                                                                                16
                                                                            }
                                                                        />
                                                                    )
                                                            }

                                                            <div className="font-medium">

                                                                Attempt
                                                                {" "}
                                                                #
                                                                {
                                                                    execution.attempt_number
                                                                }

                                                            </div>

                                                        </div>

                                                        <StatusBadge
                                                            status={
                                                                execution.status
                                                            }
                                                        />

                                                    </button>


                                                    {
                                                        expandedExecutions[
                                                            execution.id
                                                        ] && (

                                                            <>

                                                                <div className="mt-4 text-sm text-zinc-400">

                                                                    Worker:
                                                                    {" "}

                                                                    {
                                                                        execution.worker_id
                                                                        ??
                                                                        "N/A"
                                                                    }

                                                                </div>

                                                                <div className="text-sm text-zinc-500 mt-1">

                                                                    Started:
                                                                    {" "}

                                                                    {
                                                                        execution.started_at
                                                                            ? formatTimestamp(
                                                                                execution.started_at
                                                                            )
                                                                            : "N/A"
                                                                    }

                                                                </div>

                                                                <div className="text-sm text-zinc-500 mt-1">

                                                                    Completed:
                                                                    {" "}

                                                                    {
                                                                        execution.completed_at
                                                                            ? formatTimestamp(
                                                                                execution.completed_at
                                                                            )
                                                                            : "N/A"
                                                                    }

                                                                </div>


                                                                {execution.logs && (

                                                                    <div className="mt-4">

                                                                        <div
                                                                            className="
                                                                                text-xs
                                                                                text-zinc-400
                                                                                mb-2
                                                                            "
                                                                        >
                                                                            Execution Logs
                                                                        </div>

                                                                        <pre
                                                                            className="
                                                                                bg-black/70 border border-zinc-800
                                                                                rounded-xl p-3 text-xs overflow-auto
                                                                                text-emerald-300
                                                                            "
                                                                        >

                                                                            {execution.logs}

                                                                        </pre>

                                                                    </div>
                                                                )}


                                                                {execution.error_message && (

                                                                    <div
                                                                        className="
                                                                            mt-4 p-3 rounded-xl
                                                                            bg-rose-500/10 border border-rose-500/30
                                                                            text-rose-300 text-xs overflow-auto
                                                                        "
                                                                    >

                                                                        {
                                                                            execution.error_message
                                                                        }

                                                                    </div>
                                                                )}

                                                            </>

                                                        )
                                                    }

                                                </div>
                                            )
                                        )}

                                    </div>

                                </div>
                            )}

                        </div>
                    ))}

                </div>

            </div>

        </div>
    )
}

export default JobDetailsPage
