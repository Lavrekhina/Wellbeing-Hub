"use client"

import { useEffect, useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts"
import { getDashboardSummary } from "@/lib/api"

const HARDCODED_USER_ID = 1

const dummyData = [
  { date: "Feb 3", risk: 22 },
  { date: "Feb 4", risk: 25 },
  { date: "Feb 5", risk: 30 },
  { date: "Feb 6", risk: 28 },
  { date: "Feb 7", risk: 35 },
  { date: "Feb 8", risk: 45 },
  { date: "Feb 9", risk: 55 },
]

function getRiskColour(riskLevel: string) {
  if (riskLevel === "high") return "#ef4444"
  if (riskLevel === "medium") return "#f59e0b"
  return "#10b981"
}

export function BurnoutChart() {
  const [riskLevel, setRiskLevel] = useState<string>("low")

  useEffect(() => {
    async function fetchRisk() {
      try {
        const data = await getDashboardSummary(HARDCODED_USER_ID)
        setRiskLevel(data.risk_level)
      } catch {
        // keep default
      }
    }
    fetchRisk()
  }, [])

  const colour = getRiskColour(riskLevel)

  return (
    <Card className="py-6">
      <CardContent className="space-y-4">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h3 className="text-2xl font-semibold text-foreground font-sans">
              Burnout Risk Prediction
            </h3>
            <p className="text-sm font-medium text-muted-foreground">
              Monitoring your stress levels over time
            </p>
          </div>
          <Select defaultValue="7days">
            <SelectTrigger className="w-[140px] rounded-xl border-border/50 bg-card/60 backdrop-blur-sm">
              <SelectValue />
            </SelectTrigger>
            <SelectContent className="rounded-xl">
              <SelectItem value="7days">Last 7 days</SelectItem>
              <SelectItem value="14days">Last 14 days</SelectItem>
              <SelectItem value="30days">Last 30 days</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart
              data={dummyData}
              margin={{ top: 5, right: 10, left: -10, bottom: 0 }}
            >
              <defs>
                <linearGradient id="riskGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor={colour} stopOpacity={0.25} />
                  <stop offset="100%" stopColor={colour} stopOpacity={0.02} />
                </linearGradient>
              </defs>
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="hsl(270 10% 92%)"
                vertical={false}
              />
              <XAxis
                dataKey="date"
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
                  value: "Risk %",
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
                  boxShadow: "0 8px 24px rgba(139, 92, 246, 0.1)",
                }}
                formatter={(value: number | undefined) => [
                  `${value ?? 0}%`,
                  "Risk Level",
                ]}
              />
              <Area
                type="monotone"
                dataKey="risk"
                stroke={colour}
                strokeWidth={2.5}
                fill="url(#riskGradient)"
                dot={{ r: 3.5, fill: colour, strokeWidth: 0 }}
                activeDot={{
                  r: 5.5,
                  fill: colour,
                  strokeWidth: 2.5,
                  stroke: "white",
                }}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="flex flex-wrap gap-6">
          <div className="flex items-center gap-2">
            <div className="size-3 rounded-full bg-emerald-500" />
            <span className="text-xs text-muted-foreground">Low (0-30%)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="size-3 rounded-full bg-amber-500" />
            <span className="text-xs text-muted-foreground">Moderate (31-60%)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="size-3 rounded-full bg-red-500" />
            <span className="text-xs text-muted-foreground">High (61-100%)</span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}