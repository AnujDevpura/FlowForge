import {
    useEffect,
    useState,
} from "react"

import {
    fetchMetrics,
} from "../api/metrics"

function MetricsCards() {

    const [metrics, setMetrics] =
        useState<any>(null)

    useEffect(() => {

        async function loadMetrics() {

            const data =
                await fetchMetrics()

            setMetrics(data)
        }

        loadMetrics()

        const interval = setInterval(
            loadMetrics,
            3000,
        )

        return () => clearInterval(
            interval
        )

    }, [])

    if (!metrics) {
        return null
    }

    const cards = [
        {
            label: "Queued Tasks",
            value: metrics.queued_tasks,
        },
        {
            label: "Running Tasks",
            value: metrics.running_tasks,
        },
        {
            label: "Failed Tasks",
            value: metrics.failed_tasks,
        },
        {
            label: "Active Workers",
            value: metrics.active_workers,
        },
    ]

    return (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">

            {cards.map((card) => (

                <div
                    key={card.label}
                    className="
                        border
                        border-zinc-800
                        rounded-xl
                        p-5
                        bg-zinc-900
                    "
                >

                    <div className="text-zinc-400 text-sm mb-2">
                        {card.label}
                    </div>

                    <div className="text-3xl font-bold">
                        {card.value}
                    </div>

                </div>
            ))}

        </div>
    )
}

export default MetricsCards