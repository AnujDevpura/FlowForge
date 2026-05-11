import {
    useEffect,
    useState,
} from "react"

import {
    fetchWorkers,
} from "../api/workers"

type Worker = {
    id: string
    status: string
    last_heartbeat_at: string
}
import {
    formatTimestamp,
} from "../components/time"


function WorkersPage() {

    const [workers, setWorkers] =
        useState<Worker[]>([])

    useEffect(() => {

        async function loadWorkers() {

            try {

                const data =
                    await fetchWorkers()

                setWorkers(data)

            } catch (error) {

                console.error(error)
            }
        }

        loadWorkers()

        const interval = setInterval(
            loadWorkers,
            3000,
        )

        return () =>
            clearInterval(interval)

    }, [])

    return (
        <div>

            <h1 className="text-3xl font-bold mb-6">
                Workers
            </h1>

            <div className="space-y-4">

                {workers.map((worker) => (

                    <div
                        key={worker.id}
                        className="
                            border
                            border-zinc-800
                            rounded-xl
                            p-4
                            bg-zinc-900
                        "
                    >

                        <div className="text-lg font-semibold">
                            {worker.id}
                        </div>

                        <div className="text-zinc-400">
                            Status:
                            {" "}
                            {worker.status}
                        </div>

                        <div className="text-zinc-500 text-sm">
                            Last heartbeat:
                            {" "}
                            {formatTimestamp(
                                worker.last_heartbeat_at
                            )}
                        </div>

                    </div>
                ))}

            </div>

        </div>
    )
}

export default WorkersPage