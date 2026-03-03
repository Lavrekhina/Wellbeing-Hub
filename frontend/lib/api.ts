const API_BASE = "http://127.0.0.1:8000"

export async function submitCheckin(
  userId: number,
  surveyId: number,
  departmentId: number,
  consentGranted: boolean,
  answers: { question_id: number; answer_value: number }[]
) {
  const res = await fetch(`${API_BASE}/api/checkins/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: userId,
      survey_id: surveyId,
      department_id: departmentId,
      consent_granted: consentGranted,
      answers,
    }),
  })
  if (!res.ok) throw new Error("Failed to submit check-in")
  return res.json()
}

export async function getDashboardSummary(userId: number) {
  const res = await fetch(`${API_BASE}/api/dashboard/${userId}/summary`)
  if (!res.ok) throw new Error("Failed to fetch dashboard summary")
  return res.json()
}

export async function getRecommendations(userId: number) {
  const res = await fetch(`${API_BASE}/api/dashboard/${userId}/recommendations`)
  if (!res.ok) throw new Error("Failed to fetch recommendations")
  return res.json()
}

export async function getLatestConsent(userId: number) {
  const res = await fetch(`${API_BASE}/api/checkins/consent/${userId}/latest`)
  if (res.status === 404) return null
  if (!res.ok) throw new Error("Failed to fetch consent status")
  return res.json()
}

export async function getDepartmentRiskSummary(minGroupSize: number = 3) {
  const res = await fetch(`${API_BASE}/api/dashboard/hr/department-risk-summary?min_group_size=${minGroupSize}`)
  if (!res.ok) throw new Error("Failed to fetch department risk summary")
  return res.json()
}