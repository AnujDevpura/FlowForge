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
                border
                border-zinc-800
                rounded-xl
                p-6
                bg-zinc-900
                mb-8
            "
        >

            <h2 className="text-2xl font-semibold mb-4">
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
                    w-full
                    mb-4
                    p-3
                    rounded-lg
                    bg-zinc-950
                    border
                    border-zinc-700
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
                    w-full
                    p-3
                    rounded-lg
                    bg-zinc-950
                    border
                    border-zinc-700
                    font-mono
                    text-sm
                "
            />

            <button
                type="submit"
                className="
                    mt-4
                    px-5
                    py-3
                    rounded-lg
                    bg-blue-700
                    hover:bg-blue-600
                    transition
                "
            >
                Submit Workflow
            </button>

        </form>
    )
}

export default CreateJobForm