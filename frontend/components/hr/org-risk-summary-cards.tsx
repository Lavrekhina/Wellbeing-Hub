import { Card, CardContent } from "@/components/ui/card"
import { Users, Activity, ShieldAlert } from "lucide-react"

export function OrgRiskSummaryCards({ data, loading }: { data: any, loading: boolean }) {
  const departments = data?.departments || [];
  const totalResponses = departments.reduce((acc: number, dept: any) => acc + dept.response_count, 0) || 0;
  
  const avgRisk = departments.length > 0 
    ? Math.round(departments.reduce((acc: number, dept: any) => acc + dept.avg_risk_score, 0) / departments.length)
    : 0;

  const stats = [
    {
      label: "Total Participants",
      value: loading ? "..." : totalResponses,
      desc: "Across all visible departments",
      icon: Users,
      iconColor: "text-blue-600",
      iconBg: "bg-blue-50",
    },
    {
      label: "Global Risk Average",
      value: loading ? "..." : `${avgRisk}%`,
      desc: "Weighted organizational risk",
      icon: Activity,
      iconColor: "text-violet-600",
      iconBg: "bg-violet-50",
    },
    {
      label: "Privacy Exclusions",
      value: loading ? "..." : data?.excluded_departments || 0,
      desc: "Departments below min threshold",
      icon: ShieldAlert,
      iconColor: "text-amber-600",
      iconBg: "bg-amber-50",
    },
  ]

  return (
    <div className="grid grid-cols-1 gap-5 md:grid-cols-3">
      {stats.map((stat) => (
        <Card key={stat.label} className="py-6">
          <CardContent className="space-y-3">
            <div className={`flex size-12 items-center justify-center rounded-2xl ${stat.iconBg}`}>
              <stat.icon className={`size-5 ${stat.iconColor}`} />
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">{stat.label}</p>
              <p className="text-4xl font-bold text-foreground tracking-tight">{stat.value}</p>
              <p className="mt-1 text-xs text-muted-foreground">{stat.desc}</p>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}