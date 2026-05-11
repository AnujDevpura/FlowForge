type Props = {
    retryCount: number
    maxRetries: number
    status: string
}

function RetryDots({
    retryCount,
    maxRetries,
    status,
}: Props) {

    return (
        <div className="flex gap-2 mt-2">

            {Array.from({
                length: maxRetries,
            }).map((_, index) => {

                let color =
                    "bg-zinc-700"

                if (index < retryCount) {

                    color =
                        status === "FAILED"
                            ? "bg-red-500"
                            : "bg-green-500"
                }

                return (
                    <div
                        key={index}
                        className={`
                            w-3
                            h-3
                            rounded-full
                            ${color}
                        `}
                    />
                )
            })}

        </div>
    )
}

export default RetryDots