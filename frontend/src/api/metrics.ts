import api from "./client"

export async function fetchMetrics() {

    const response = await api.get(
        "/metrics/"
    )

    return response.data
}