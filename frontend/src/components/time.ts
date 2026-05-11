export function formatTimestamp(
    timestamp: string | null,
) {

    if (!timestamp) {
        return "N/A"
    }

    const date =
        new Date(timestamp)

    const now =
        new Date()

    const diffMs =
        now.getTime()
        -
        date.getTime()

    const diffSeconds =
        Math.floor(diffMs / 1000)

    const diffMinutes =
        Math.floor(diffSeconds / 60)

    const diffHours =
        Math.floor(diffMinutes / 60)

    const diffDays =
        Math.floor(diffHours / 24)

    let relative = ""

    if (diffSeconds < 60) {

        relative =
            `${diffSeconds}s ago`

    } else if (
        diffMinutes < 60
    ) {

        relative =
            `${diffMinutes}m ago`

    } else if (
        diffHours < 24
    ) {

        relative =
            `${diffHours}h ago`

    } else {

        relative =
            `${diffDays}d ago`
    }

    const absolute =
        date.toLocaleString()

    return (
        `${relative} • ${absolute}`
    )
}