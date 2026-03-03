"use client"

import { useEffect, useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Flame, Activity, Moon, Heart } from "lucide-react"
import { getDashboardSummary } from "@/lib/api"

const HARDCODED_USER_ID = 1

export function StatCards() {
  const [riskScore, setRiskScore] = useState<number | null>(null)
  const [riskLevel, setRiskLevel] = useState<string | null>(null)

  useEffect(() => {
    async function fetchSummary() {
      try {
        const data = await getDashboardSummary(HARDCODED_USER_ID)
        setRiskScore(data.risk_score)
        setRiskLevel(data.risk_level)
      } catch {
        // keep dummy data if fetch fails
      }
    }
    fetchSummary()
  }, [])

  const wellbeingValue =
    riskScore !== null ? `${(100 - riskScore).toFixed(0)}/100` : "--";
  const wellbeingChange =
    riskLevel !== null
      ? riskLevel === "low"
        ? "Low risk — keep it up!"
        : riskLevel === "medium"
          ? "Moderate risk — check in regularly"
          : "High risk — please seek support"
      : "No check-in yet";

  const wellbeingChangeColor = riskLevel === "high"
    ? "text-red-500"
    : riskLevel === "medium"
    ? "text-amber-500"
    : "text-emerald-600"

  const stats = [
    {
      label: "Current Streak",
      value: "7 days",
      change: "+2 from last week",
      changeColor: "text-emerald-600",
      icon: Flame,
      iconColor: "text-orange-500",
      iconBg: "bg-orange-50",
    },
    {
      label: "Activities Completed",
      value: "24",
      change: "This week",
      changeColor: "text-muted-foreground",
      icon: Activity,
      iconColor: "text-blue-600",
      iconBg: "bg-blue-50",
    },
    {
      label: "Avg Sleep",
      value: "7.5 hrs",
      change: "+0.5 hrs improvement",
      changeColor: "text-emerald-600",
      icon: Moon,
      iconColor: "text-indigo-600",
      iconBg: "bg-indigo-50",
    },
    {
      label: "Wellbeing Score",
      value: wellbeingValue,
      change: wellbeingChange,
      changeColor: wellbeingChangeColor,
      icon: Heart,
      iconColor: "text-pink-500",
      iconBg: "bg-pink-50",
    },
  ]

  return (
    <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-4">
      {stats.map((stat) => (
        <Card key={stat.label} className="py-6">
          <CardContent className="space-y-3">
            <div className={`flex size-12 items-center justify-center rounded-2xl ${stat.iconBg}`}>
              <stat.icon className={`size-5 ${stat.iconColor}`} />
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">{stat.label}</p>
              <p className="text-4xl font-bold text-foreground tracking-tight">{stat.value}</p>
              <p className={`mt-1 text-xs font-medium ${stat.changeColor}`}>{stat.change}</p>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}