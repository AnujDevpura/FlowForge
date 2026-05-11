import api from "./client"

export async function fetchJobDetails(
    jobId: string,
) {

    const response = await api.get(
        `/jobs/${jobId}`
    )

    return response.data
}