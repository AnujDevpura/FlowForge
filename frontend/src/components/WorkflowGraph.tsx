import dagre from "dagre"

import ReactFlow, {
    Background,
    Controls,
} from "reactflow"

import type {
    Task,
    Dependency,
} from "../types/job"

type Props = {
    tasks: Task[]

    dependencies: Dependency[]

    isBlockedTask: (
        task: Task
    ) => boolean
}

const dagreGraph =
    new dagre.graphlib.Graph()

dagreGraph.setDefaultEdgeLabel(
    () => ({})
)

const nodeWidth = 220

const nodeHeight = 80


function getNodeColor(
    status: string,
) {

    switch (status) {

        case "SUCCESS":
            return "#14532d"

        case "FAILED":
            return "#7f1d1d"

        case "RUNNING":
            return "#1d4ed8"

        case "QUEUED":
            return "#78350f"

        case "BLOCKED":
            return "#52525b"

        default:
            return "#27272a"
    }
}


function WorkflowGraph({
    tasks,
    dependencies,
    isBlockedTask,
}: Props) {

    dagreGraph.setGraph({
        rankdir: "TB",
    })

    tasks.forEach((task) => {

        dagreGraph.setNode(
            task.id,
            {
                width: nodeWidth,
                height: nodeHeight,
            }
        )
    })

    dependencies.forEach((dep) => {

        dagreGraph.setEdge(
            dep.depends_on_task_id,
            dep.task_id,
        )
    })

    dagre.layout(dagreGraph)

    const nodes = tasks.map((task) => {

        const node =
            dagreGraph.node(task.id)

        const displayStatus =
            isBlockedTask(task)
                ? "BLOCKED"
                : task.status

        return {

            id: task.id,

            data: {
                label: (
                    <div>

                        <div
                            style={{
                                fontSize: 16,
                                marginBottom: 6,
                            }}
                        >
                            {task.name}
                        </div>

                        <div
                            style={{
                                opacity: 0.8,
                                fontSize: 12,
                            }}
                        >
                            {displayStatus}
                        </div>

                    </div>
                ),
            },

            position: {
                x: node.x,
                y: node.y,
            },

            style: {
                padding: 12,

                borderRadius: 16,

                border:
                    "1px solid #52525b",

                background:
                    getNodeColor(
                        displayStatus
                    ),

                color: "white",

                width: nodeWidth,

                fontWeight: 600,
                boxShadow: "0 10px 28px -18px rgba(6, 182, 212, 0.8)",
            },
        }
    })

    const edges = dependencies.map(
        (dep) => ({

            id:
                `${dep.depends_on_task_id}-${dep.task_id}`,

            source:
                dep.depends_on_task_id,

            target:
                dep.task_id,

            animated: true,
        })
    )

    return (

        <div
            className="
                h-[500px]
                border border-zinc-800/80
                rounded-2xl
                overflow-hidden
                bg-zinc-950/80
            "
        >

            <ReactFlow
                nodes={nodes}
                edges={edges}
                fitView
            >

                <Background />

                <Controls />

            </ReactFlow>

        </div>
    )
}

export default WorkflowGraph
