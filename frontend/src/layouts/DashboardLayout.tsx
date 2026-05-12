import { NavLink } from "react-router-dom"

type Props = {
    children: React.ReactNode
}

function DashboardLayout({
    children,
}: Props) {

    return (
        <div className="min-h-screen flex flex-col md:flex-row text-white">

            <aside
                className="
                    w-full
                    md:w-72
                    border-b
                    md:border-b-0
                    md:border-r
                    border-zinc-800/70
                    bg-zinc-950/75
                    backdrop-blur
                    p-5
                "
            >

                <div className="mb-8 rounded-2xl border border-zinc-800 bg-zinc-900/70 p-4">
                    <h1 className="text-3xl font-black tracking-tight text-zinc-100">
                        FlowForge
                    </h1>
                    <p className="mt-2 text-xs uppercase tracking-[0.18em] text-zinc-500">
                        Distributed Workflow Engine
                    </p>
                </div>

                <nav className="flex flex-row md:flex-col gap-3">

                    <NavLink
                        to="/"
                        end
                        className={({ isActive }) =>
                            `
                                rounded-xl
                                px-4
                                py-3
                                font-semibold
                                transition
                                border
                                ${
                                    isActive
                                        ? "border-cyan-500/60 bg-cyan-500/15 text-cyan-200"
                                        : "border-zinc-800 bg-zinc-900/60 text-zinc-300 hover:border-zinc-700 hover:text-zinc-100"
                                }
                            `
                        }
                    >
                        Jobs
                    </NavLink>

                    <NavLink
                        to="/workers"
                        className={({ isActive }) =>
                            `
                                rounded-xl
                                px-4
                                py-3
                                font-semibold
                                transition
                                border
                                ${
                                    isActive
                                        ? "border-cyan-500/60 bg-cyan-500/15 text-cyan-200"
                                        : "border-zinc-800 bg-zinc-900/60 text-zinc-300 hover:border-zinc-700 hover:text-zinc-100"
                                }
                            `
                        }
                    >
                        Workers
                    </NavLink>

                </nav>

            </aside>

            <main className="flex-1 p-4 md:p-8">
                {children}
            </main>

        </div>
    )
}

export default DashboardLayout
