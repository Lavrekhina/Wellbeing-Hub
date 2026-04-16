const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000"
const ADMIN_SECRET_KEY = process.env.NEXT_PUBLIC_ADMIN_API_KEY || ""

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

export async function getAdminOverview() {
  const res = await fetch(`${API_BASE}/api/admin/overview`, {
    headers: { "X-Admin-Key": ADMIN_SECRET_KEY },
  })
  if (!res.ok) throw new Error("Failed to fetch admin overview")
  return res.json()
}

export async function getAdminRecentAssessments(limit = 50) {
  const res = await fetch(`${API_BASE}/api/admin/assessments/recent?limit=${limit}`, {
    headers: { "X-Admin-Key": ADMIN_SECRET_KEY },
  })
  if (!res.ok) throw new Error("Failed to fetch recent assessments")
  return res.json()
}

export async function getMLMetrics() {
  const res = await fetch(`${API_BASE}/api/metrics/risk-classifier`)
  if (!res.ok) throw new Error("Failed to fetch ML metrics")
  return res.json()
}