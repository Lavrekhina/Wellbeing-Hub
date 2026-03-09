"use client"

import { useEffect, useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts"
import { getDepartmentRiskSummary } from "@/lib/api"

const fallbackData = [
  { week: "Week 1", avgRisk: 28 },
  { week: "Week 2", avgRisk: 32 },
  { week: "Week 3", avgRisk: 30 },
  { week: "Week 4", avgRisk: 38 },
  { week: "Week 5", avgRisk: 35 },
  { week: "Week 6", avgRisk: 42 },
  { week: "Week 7", avgRisk: 39 },
]

export function TeamTrendChart() {
  const [data, setData] = useState(fallbackData)
  const [usingRealData, setUsingRealData] = useState(false)

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await getDepartmentRiskSummary(3)
        if (response.departments && response.departments.length > 0) {
          const mapped = response.departments.map((dept: {
            department_label: string
            avg_risk_score: number
          }, index: number) => ({
            week: dept.department_label,
            avgRisk: Math.round(dept.avg_risk_score),
          }))
          setData(mapped)
          setUsingRealData(true)
        }
      } catch {
        // keep fallback
      }
    }
    fetchData()
  }, [])

  return (
    <Card className="py-6">
      <CardContent className="space-y-4">
        <div className="flex items-start justify-between">
          <div>
            <h3 className="text-xl font-semibold text-foreground">
              Team Wellbeing Trend
            </h3>
            <p className="text-sm text-muted-foreground font-medium">
              Average anonymised risk score across department — last 7 weeks
            </p>
          </div>
          {!usingRealData && (
            <span className="text-xs text-muted-foreground italic">
              Sample data
            </span>
          )}
        </div>
        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart
              data={data}
              margin={{ top: 5, right: 10, left: -10, bottom: 0 }}
            >
              <defs>
                <linearGradient id="teamRiskGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#7c3aed" stopOpacity={0.2} />
                  <stop offset="100%" stopColor="#7c3aed" stopOpacity={0.02} />
                </linearGradient>
              </defs>
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="hsl(270 10% 92%)"
                vertical={false}
              />
              <XAxis
                dataKey="week"
                axisLine={false}
                tickLine={false}
                tick={{ fontSize: 12, fill: "hsl(270 5% 50%)" }}
                dy={10}
              />
              <YAxis
                domain={[0, 100]}
                ticks={[0, 25, 50, 75, 100]}
                axisLine={false}
                tickLine={false}
                tick={{ fontSize: 12, fill: "hsl(270 5% 50%)" }}
                dx={-5}
                label={{
                  value: "Avg Risk %",
                  angle: -90,
                  position: "insideLeft",
                  offset: 15,
                  style: { fontSize: 12, fill: "hsl(270 5% 50%)" },
                }}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "rgba(255, 255, 255, 0.9)",
                  backdropFilter: "blur(8px)",
                  border: "1px solid rgba(139, 92, 246, 0.15)",
                  borderRadius: "16px",
                  fontSize: "13px",
                }}
                formatter={(value: number | undefined) => [
                  `${value ?? 0}%`,
                  "Avg Risk",
                ]}
              />
              <Area
                type="monotone"
                dataKey="avgRisk"
                stroke="#7c3aed"
                strokeWidth={2.5}
                fill="url(#teamRiskGradient)"
                dot={{ r: 3.5, fill: "#7c3aed", strokeWidth: 0 }}
                activeDot={{
                  r: 5.5,
                  fill: "#7c3aed",
                  strokeWidth: 2.5,
                  stroke: "white",
                }}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  )
}