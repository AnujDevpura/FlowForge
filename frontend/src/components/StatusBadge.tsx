type Props = {
    status: string
}

function StatusBadge({
    status,
}: Props) {

    const getClasses = () => {

        switch (status) {

            case "SUCCESS":
                return `
                    bg-emerald-500/15
                    text-emerald-300
                    border-emerald-500/40
                `

            case "FAILED":
                return `
                    bg-rose-500/15
                    text-rose-300
                    border-rose-500/40
                `

            case "RUNNING":
                return `
                    bg-cyan-500/15
                    text-cyan-300
                    border-cyan-500/40
                `

            case "QUEUED":
                return `
                    bg-amber-500/15
                    text-amber-300
                    border-amber-500/40
                `
            
            case "BLOCKED":
                return `bg-zinc-700/40
                    text-zinc-300
                    border-zinc-600`

            default:
                return `
                    bg-zinc-700/40
                    text-zinc-300
                    border-zinc-600
                `
        }
    }

    return (
        <span
            className={`
                px-3
                py-1
                rounded-full
                text-sm
                border
                font-semibold
                tracking-wide
                ${getClasses()}
            `}
        >

            {status}

        </span>
    )
}

export default StatusBadge
