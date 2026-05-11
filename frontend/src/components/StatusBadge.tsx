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
                    bg-green-900
                    text-green-300
                    border-green-700
                `

            case "FAILED":
                return `
                    bg-red-900
                    text-red-300
                    border-red-700
                `

            case "RUNNING":
                return `
                    bg-blue-900
                    text-blue-300
                    border-blue-700
                `

            case "QUEUED":
                return `
                    bg-yellow-900
                    text-yellow-300
                    border-yellow-700
                `
            
            case "BLOCKED":
                return `bg-zinc-800
                    text-zinc-300
                    border-zinc-700`

            default:
                return `
                    bg-zinc-800
                    text-zinc-300
                    border-zinc-700
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
                font-medium
                ${getClasses()}
            `}
        >

            {status}

        </span>
    )
}

export default StatusBadge