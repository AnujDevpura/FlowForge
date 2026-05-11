import api from "./client"

export async function createJob(
    payload: any,
) {

    const response = await api.post(
        "/jobs/",
        payload,
    )

    return response.data
}