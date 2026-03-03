"use client"

import { useEffect, useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { getDepartmentRiskSummary } from "@/lib/api"

const fallbackData = [
  {
    label: "Low Risk",
    value: "62%",
    count: "31 employees",
    color: "text-emerald-600",
    bg: "bg-emerald-50",
    dot: "bg-emerald-500",
  },
  {
    label: "Moderate Risk",
    value: "28%",
    count: "14 employees",
    color: "text-amber-600",
    bg: "bg-amber-50",
    dot: "bg-amber-500",
  },
  {
    label: "High Risk",
    value: "10%",
    count: "5 employees",
    color: "text-red-600",
    bg: "bg-red-50",
    dot: "bg-red-500",
  },
]

export function DepartmentRiskOverview() {
  const [riskData, setRiskData] = useState(fallbackData)
  const [usingRealData, setUsingRealData] = useState(false)

  useEffect(() => {
    async function fetchData() {
      try {
        const data = await getDepartmentRiskSummary(3)
        if (data.departments && data.departments.length > 0) {
          const mapped = data.departments.map((dept: {
            department_label: string
            avg_risk_score: number
            high_risk_ratio: number
            response_count: number
            risk_level_breakdown: Record<string, number>
          }) => {
            const total = dept.response_count
            const low = Math.round((dept.risk_level_breakdown?.low ?? 0) * total)
            const medium = Math.round((dept.risk_level_breakdown?.medium ?? 0) * total)
            const high = Math.round((dept.risk_level_breakdown?.high ?? 0) * total)
            return [
              {
                label: "Low Risk",
                value: `${Math.round((dept.risk_level_breakdown?.low ?? 0) * 100)}%`,
                count: `${low} employees`,
                color: "text-emerald-600",
                bg: "bg-emerald-50",
                dot: "bg-emerald-500",
              },
              {
                label: "Moderate Risk",
                value: `${Math.round((dept.risk_level_breakdown?.medium ?? 0) * 100)}%`,
                count: `${medium} employees`,
                color: "text-amber-600",
                bg: "bg-amber-50",
                dot: "bg-amber-500",
              },
              {
                label: "High Risk",
                value: `${Math.round((dept.risk_level_breakdown?.high ?? 0) * 100)}%`,
                count: `${high} employees`,
                color: "text-red-600",
                bg: "bg-red-50",
                dot: "bg-red-500",
              },
            ]
          })
          setRiskData(mapped[0])
          setUsingRealData(true)
        }
      } catch {
        // keep fallback data
      }
    }
    fetchData()
  }, [])

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold text-foreground">
          Department Risk Distribution
        </h3>
        {!usingRealData && (
          <span className="text-xs text-muted-foreground italic">
            Sample data — live data available with more users
          </span>
        )}
      </div>
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-3">
        {riskData.map((item) => (
          <Card key={item.label} className="py-6">
            <CardContent className="space-y-3">
              <div className="flex items-center gap-2">
                <div className={`size-3 rounded-full ${item.dot}`} />
                <p className="text-sm font-medium text-muted-foreground">
                  {item.label}
                </p>
              </div>
              <p className={`text-4xl font-bold ${item.color}`}>
                {item.value}
              </p>
              <p className="text-xs text-muted-foreground">{item.count}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}