import {
    useState,
} from "react"

import {
    createJob,
} from "../api/createJob"

function CreateJobForm() {

    const [jobName, setJobName] =
        useState("")

    const [workflowJson, setWorkflowJson] =
        useState(`{
  "tasks": [
    {
      "name": "fetch_data",
      "payload": {
        "type": "http",
        "url": "https://jsonplaceholder.typicode.com/todos/1"
      }
    }
  ]
}`)

    async function handleSubmit(
        e: React.FormEvent,
    ) {

        e.preventDefault()

        try {

            const workflow = JSON.parse(
                workflowJson
            )

            await createJob({
                name: jobName,
                ...workflow,
            })

            alert("Job created successfully")

            setJobName("")

        } catch (error) {

            console.error(error)

            alert(
                "Invalid workflow JSON"
            )
        }
    }

    return (
        <form
            onSubmit={handleSubmit}
            className="
                border border-zinc-800/80 rounded-2xl p-6 md:p-7
                bg-zinc-900/70 backdrop-blur
                mb-8 shadow-[0_16px_44px_-30px_rgba(6,182,212,0.45)]
            "
        >

            <h2 className="text-2xl font-black tracking-tight mb-5">
                Create Job
            </h2>

            <input
                type="text"
                placeholder="Job Name"
                value={jobName}
                onChange={(e) =>
                    setJobName(
                        e.target.value
                    )
                }
                className="
                    w-full mb-4 p-3 rounded-xl
                    bg-zinc-950/80 border border-zinc-700
                    text-zinc-100 placeholder:text-zinc-500
                    focus:outline-none focus:ring-2 focus:ring-cyan-500/40
                "
            />

            <textarea
                value={workflowJson}
                onChange={(e) =>
                    setWorkflowJson(
                        e.target.value
                    )
                }
                rows={14}
                className="
                    w-full p-3 rounded-xl bg-zinc-950/80 border border-zinc-700
                    font-mono text-sm text-zinc-200
                    focus:outline-none focus:ring-2 focus:ring-cyan-500/40
                "
            />

            <button
                type="submit"
                className="
                    mt-4 px-5 py-3 rounded-xl
                    bg-cyan-600 text-cyan-950 font-bold
                    hover:bg-cyan-500 transition
                "
            >
                Submit Workflow
            </button>

        </form>
    )
}

export default CreateJobForm
