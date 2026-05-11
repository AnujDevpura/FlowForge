import api from "./client"

export async function fetchJobs() {

  const response = await api.get("/jobs/")

  return response.data
}