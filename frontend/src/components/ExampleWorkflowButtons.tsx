import {
    createJob,
} from "../api/createJob"

function ExampleWorkflowButtons() {

    async function runContextWorkflow() {

        await createJob({

            name: "enterprise_data_pipeline",

            tasks: [

                {
                    name: "fetch_users",

                    payload: {
                        type: "http",

                        url:
                            "https://jsonplaceholder.typicode.com/users",
                    },

                    dependencies: [],

                    max_retries: 3,
                },

                {
                    name: "validate_data",

                    payload: {
                        type: "print",

                        message:
                            "Validating incoming user records",
                    },

                    dependencies: [
                        "fetch_users",
                    ],

                    max_retries: 3,
                },

                {
                    name: "transform_data",

                    payload: {
                        type: "print",

                        message:
                            "Transforming and normalizing data",
                    },

                    dependencies: [
                        "validate_data",
                    ],

                    max_retries: 3,
                },

                {
                    name: "analytics_engine",

                    payload: {
                        type: "print",

                        message:
                            "Generating analytics metrics",
                    },

                    dependencies: [
                        "transform_data",
                    ],

                    max_retries: 3,
                },

                {
                    name: "enrich_data",

                    payload: {
                        type: "http",

                        url:
                            "https://jsonplaceholder.typicode.com/posts",
                    },

                    dependencies: [
                        "transform_data",
                    ],

                    max_retries: 3,
                },

                {
                    name: "generate_report",

                    payload: {
                        type: "print",

                        message:
                            "Building enterprise workflow report",
                    },

                    dependencies: [
                        "transform_data",
                    ],

                    max_retries: 3,
                },

                {
                    name: "merge_results",

                    payload: {
                        type: "print",

                        message:
                            "Aggregating pipeline outputs",
                    },

                    dependencies: [
                        "analytics_engine",
                        "enrich_data",
                        "generate_report",
                    ],

                    max_retries: 3,
                },

                {
                    name: "notify_completion",

                    payload: {
                        type: "print",

                        message:
                            "Sending workflow success notification",
                    },

                    dependencies: [
                        "merge_results",
                    ],

                    max_retries: 3,
                },
            ],
        })
    }

    async function runFailureWorkflow() {

        await createJob({

            name: "failure_recovery_pipeline",

            tasks: [

                {
                    name: "fetch_source_data",

                    payload: {
                        type: "http",

                        url:
                            "https://jsonplaceholder.typicode.com/todos/1",
                    },

                    dependencies: [],

                    max_retries: 3,
                },

                {
                    name: "process_batch",

                    payload: {
                        type: "print",

                        message:
                            "Processing incoming workflow batch",
                    },

                    dependencies: [
                        "fetch_source_data",
                    ],

                    max_retries: 3,
                },

                {
                    name: "unstable_api",

                    payload: {
                        type: "python",
                    },

                    dependencies: [
                        "process_batch",
                    ],

                    max_retries: 3,
                },

                {
                    name: "generate_backup",

                    payload: {
                        type: "print",

                        message:
                            "Generating backup recovery dataset",
                    },

                    dependencies: [
                        "process_batch",
                    ],

                    max_retries: 2,
                },

                {
                    name: "recovery_handler",

                    payload: {
                        type: "print",

                        message:
                            "Executing workflow recovery procedures",
                    },

                    dependencies: [
                        "unstable_api",
                    ],

                    max_retries: 1,
                },

                {
                    name: "failure_notification",

                    payload: {
                        type: "print",

                        message:
                            "Dispatching workflow failure notification",
                    },

                    dependencies: [
                        "recovery_handler",
                    ],

                    max_retries: 1,
                },
            ],
        })
    }

    return (
        <div className="mb-8 flex gap-4 flex-wrap">

            <button
                onClick={runContextWorkflow}
                className="
                    px-4
                    py-3
                    rounded-lg
                    bg-green-700
                    hover:bg-green-600
                "
            >
                Run Context Workflow
            </button>

            <button
                onClick={runFailureWorkflow}
                className="
                    px-4
                    py-3
                    rounded-lg
                    bg-red-700
                    hover:bg-red-600
                "
            >
                Run Failure Demo
            </button>

        </div>
    )
}

export default ExampleWorkflowButtons