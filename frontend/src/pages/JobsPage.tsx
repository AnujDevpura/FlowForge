import { useEffect, useState } from "react"
import { Link } from "react-router-dom"

import { fetchJobs } from "../api/jobs"

import StatusBadge from "../components/StatusBadge"
import CreateJobForm from "../components/CreateJobForm"
import ExampleWorkflowButtons from "../components/ExampleWorkflowButtons"
import MetricsCards from "../components/MetricsCards"
import {
    formatTimestamp,
} from "../components/time"


type Job = {
    id: string
    name: string
    status: string
    created_at: string
}

function JobsPage() {

    const [jobs, setJobs] =
        useState<Job[]>([])

    const [filter, setFilter] =
        useState("ALL")

    const [search, setSearch] =
        useState("")

    useEffect(() => {

        async function loadJobs() {

            try {

                const data =
                    await fetchJobs()

                setJobs(data)

            } catch (error) {

                console.error(error)
            }
        }

        loadJobs()

        const interval = setInterval(
            loadJobs,
            3000,
        )

        return () => clearInterval(
            interval
        )

    }, [])

    const filteredJobs = jobs.filter(
        (job) => {

            const matchesStatus =
                filter === "ALL"
                ||
                job.status === filter

            const matchesSearch =
                job.name
                    .toLowerCase()
                    .includes(
                        search.toLowerCase()
                    )

            return (
                matchesStatus
                &&
                matchesSearch
            )
        }
    )

    return (
        <div>

            <MetricsCards />

            <CreateJobForm />

            <ExampleWorkflowButtons />

            <h1 className="text-3xl font-bold mb-6">
                Jobs
            </h1>

            <div className="flex gap-4 mb-6 flex-wrap">

                <input
                    type="text"
                    placeholder="Search jobs..."
                    value={search}
                    onChange={(e) =>
                        setSearch(
                            e.target.value
                        )
                    }
                    className="
                        px-4
                        py-2
                        rounded-lg
                        bg-zinc-900
                        border
                        border-zinc-700
                    "
                />

                {[
                    "ALL",
                    "RUNNING",
                    "SUCCESS",
                    "FAILED",
                    "QUEUED",
                ].map((status) => (

                    <button
                        key={status}
                        onClick={() =>
                            setFilter(status)
                        }
                        className={`
                            px-4
                            py-2
                            rounded-lg
                            border

                            ${
                                filter === status
                                    ? `
                                        bg-blue-700
                                        border-blue-600
                                      `
                                    : `
                                        bg-zinc-900
                                        border-zinc-700
                                      `
                            }
                        `}
                    >

                        {status}

                    </button>
                ))}

            </div>

            <div className="space-y-4">

                {filteredJobs.map((job) => (

                    <Link
                        key={job.id}
                        to={`/jobs/${job.id}`}
                    >

                        <div
                            className="
                                border
                                border-zinc-800
                                rounded-xl
                                p-4
                                bg-zinc-900
                                hover:border-zinc-600
                                transition
                                cursor-pointer
                            "
                        >

                            <div className="text-xl font-semibold mb-2">
                                {job.name}
                            </div>

                            <div className="mb-2">
                                <StatusBadge
                                    status={job.status}
                                />
                            </div>

                            <div className="text-zinc-500 text-sm">
                                Created:
                                {" "}
                                {formatTimestamp(
                                    job.created_at
                                )}
                            </div>

                        </div>

                    </Link>
                ))}

            </div>

        </div>
    )
}

export default JobsPage