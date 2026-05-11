import api from "./client"

export async function fetchWorkers() {

    const response = await api.get(
        "/workers/"
    )

    return response.data
}