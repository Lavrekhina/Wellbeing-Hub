import Link from "next/link"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { CheckCircle2, Clock } from "lucide-react"

const activities = [
  {
    title: "Morning Meditation",
    time: "8:30 AM",
    duration: "10 minutes",
    tag: "Meditation",
    tagColor: "bg-emerald-50 text-emerald-700 border-emerald-200/60",
    completed: true,
    href: "/activities/meditation",
  },
  {
    title: "Gratitude Journal",
    time: "9:15 AM",
    duration: "5 minutes",
    tag: "Journal",
    tagColor: "bg-blue-50 text-blue-700 border-blue-200/60",
    completed: true,
    href: "/journal",
  },
  {
    title: "Breathing Exercise",
    time: "12:00 PM",
    duration: "5 minutes",
    tag: "Breathing",
    tagColor: "bg-pink-50 text-pink-700 border-pink-200/60",
    completed: true,
    href: "/activities/breathing",
  },
  {
    title: "Evening Walk",
    time: "6:00 PM",
    duration: "20 minutes",
    tag: "Exercise",
    tagColor: "bg-gray-50 text-gray-700 border-gray-200/60",
    completed: false,
    href: "/activities/exercise",
  },
]

export function TodaysActivities() {
  return (
    <Card className="py-6">
      <CardContent className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-2xl font-semibold text-foreground font-sans">{"Today's Activities"}</h3>
          <Link
            href="/activities"
            className="text-sm font-semibold text-primary hover:text-primary/80 transition-colors duration-200"
          >
            View All
          </Link>
        </div>

        <div className="flex flex-col gap-4">
          {activities.map((activity) => (
            <Link
              key={activity.title}
              href={activity.href}
              className="flex items-center gap-3 rounded-2xl p-2 -mx-2 transition-all duration-200 hover:bg-accent/50"
            >
              <div className="shrink-0">
                {activity.completed ? (
                  <CheckCircle2 className="size-8 text-emerald-500" />
                ) : (
                  <Clock className="size-8 text-muted-foreground" />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-semibold text-foreground">{activity.title}</p>
                <p className="text-xs text-muted-foreground">
                  {activity.time} &middot; {activity.duration}
                </p>
              </div>
              <Badge
                variant="outline"
                className={`shrink-0 rounded-xl ${activity.tagColor}`}
              >
                {activity.tag}
              </Badge>
            </Link>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
