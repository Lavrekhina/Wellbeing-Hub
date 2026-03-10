import { Card, CardContent } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"

export function DepartmentComparisonList({ departments, loading }: { departments: any[], loading: boolean }) {
  if (loading) return <div className="text-sm text-muted-foreground">Loading organization data...</div>
  
  if (departments.length === 0) {
    return (
      <Card className="p-12 text-center border-dashed">
        <p className="text-muted-foreground">No data meets the minimum privacy threshold yet.</p>
      </Card>
    )
  }

  return (
    <div className="grid grid-cols-1 gap-5 xl:grid-cols-2">
      {departments.map((dept) => (
        <Card key={dept.department_label} className="py-6 transition-all hover:border-primary/20">
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <Badge variant="outline" className="rounded-lg bg-secondary/50 text-secondary-foreground">
                  {dept.department_label.toUpperCase()}
                </Badge>
                <p className="text-xs text-muted-foreground">{dept.response_count} Anonymized Respondents</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-semibold">Avg Risk Score</p>
                <p className="text-2xl font-bold text-primary">{Math.round(dept.avg_risk_score)}%</p>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-xs font-medium">
                <span>Risk Concentration</span>
                <span className={dept.high_risk_ratio > 0.2 ? "text-red-500" : "text-emerald-600"}>
                  {Math.round(dept.high_risk_ratio * 100)}% High Risk Ratio
                </span>
              </div>
              <Progress value={dept.avg_risk_score} className="h-2 bg-secondary" />
            </div>

            <div className="grid grid-cols-3 gap-2 pt-2 border-t border-border/50">
                <div className="text-center">
                    <p className="text-[10px] text-muted-foreground uppercase font-bold">Low</p>
                    <p className="text-sm font-semibold text-emerald-600">{dept.risk_level_breakdown.low}</p>
                </div>
                <div className="text-center">
                    <p className="text-[10px] text-muted-foreground uppercase font-bold">Medium</p>
                    <p className="text-sm font-semibold text-amber-500">{dept.risk_level_breakdown.medium}</p>
                </div>
                <div className="text-center">
                    <p className="text-[10px] text-muted-foreground uppercase font-bold">High</p>
                    <p className="text-sm font-semibold text-red-500">{dept.risk_level_breakdown.high}</p>
                </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}