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
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 mb-8">

            {cards.map((card) => (

                <div
                    key={card.label}
                    className="
                        border border-zinc-800/90 rounded-2xl p-5
                        bg-gradient-to-b from-zinc-900/90 to-zinc-950/90
                        shadow-[0_12px_40px_-24px_rgba(20,184,166,0.6)]
                    "
                >

                    <div className="text-zinc-400 text-xs mb-3 uppercase tracking-[0.16em]">
                        {card.label}
                    </div>

                    <div className="text-4xl font-black tracking-tight text-zinc-100">
                        {card.value}
                    </div>

                </div>
            ))}

        </div>
    )
}

export default MetricsCards
