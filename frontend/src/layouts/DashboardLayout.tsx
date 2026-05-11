import { Link } from "react-router-dom"

type Props = {
    children: React.ReactNode
}

function DashboardLayout({
    children,
}: Props) {

    return (
        <div className="min-h-screen flex bg-zinc-950 text-white">

            <aside className="w-64 border-r border-zinc-800 p-4">

                <h1 className="text-2xl font-bold mb-8">
                    FlowForge
                </h1>

                <nav className="flex flex-col gap-4">

                    <Link to="/">
                        Jobs
                    </Link>

                    <Link to="/workers">
                        Workers
                    </Link>

                </nav>

            </aside>

            <main className="flex-1 p-6">
                {children}
            </main>

        </div>
    )
}

export default DashboardLayout