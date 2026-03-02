import { Card, CardContent } from "@/components/ui/card"

const riskData = [
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
  return (
    <div className="space-y-4">
      <h3 className="text-xl font-semibold text-foreground">
        Department Risk Distribution
      </h3>
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