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
        <div className="mx-auto max-w-7xl">

            <MetricsCards />

            <CreateJobForm />

            <ExampleWorkflowButtons />

            <h1 className="text-3xl md:text-4xl font-black tracking-tight mb-6">
                Jobs
            </h1>

            <div className="flex gap-3 mb-6 flex-wrap">

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
                        px-4 py-2 rounded-xl bg-zinc-900/80 border border-zinc-700
                        text-zinc-100 placeholder:text-zinc-500
                        focus:outline-none focus:ring-2 focus:ring-cyan-500/40
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
                            px-4 py-2 rounded-xl border font-medium transition

                            ${
                                filter === status
                                    ? `
                                        bg-cyan-600/25
                                        border-cyan-500/50
                                        text-cyan-200
                                      `
                                    : `
                                        bg-zinc-900/70
                                        border-zinc-700
                                        text-zinc-300
                                        hover:text-zinc-100
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
                                border border-zinc-800/90 rounded-2xl p-5
                                bg-gradient-to-b from-zinc-900/90 to-zinc-950/90
                                hover:border-cyan-600/50 transition
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
                {filteredJobs.length === 0 && (
                    <div className="rounded-2xl border border-zinc-800 bg-zinc-900/70 p-6 text-zinc-400">
                        No jobs match the current filters.
                    </div>
                )}

            </div>

        </div>
    )
}

export default JobsPage
