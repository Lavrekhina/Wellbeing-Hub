import { Card, CardContent } from "@/components/ui/card"
import { Flame, Activity, Moon, Heart } from "lucide-react"

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
    value: "8.2/10",
    change: "Above your average",
    changeColor: "text-emerald-600",
    icon: Heart,
    iconColor: "text-pink-500",
    iconBg: "bg-pink-50",
  },
]

export function StatCards() {
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
