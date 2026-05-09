import Link from "next/link"
import { Card, CardContent } from "@/components/ui/card"
import { Video, FileText, Headphones, Heart, ExternalLink } from "lucide-react"

const resources = [
  {
    title: "Understanding Anxiety",
    desc: "Learn coping strategies for managing anxiety",
    time: "12 min",
    icon: Video,
    iconColor: "text-red-500",
    iconBg: "bg-red-50",
    href: "/resources/understanding-anxiety",
  },
  {
    title: "Sleep Hygiene Guide",
    desc: "Tips for better sleep quality",
    time: "5 min read",
    icon: FileText,
    iconColor: "text-emerald-600",
    iconBg: "bg-emerald-50",
    href: "/resources/sleep-hygiene",
  },
  {
    title: "Calm Mind Meditation",
    desc: "Guided meditation for stress relief",
    time: "15 min",
    icon: Headphones,
    iconColor: "text-primary",
    iconBg: "bg-secondary",
    href: "/resources/calm-mind",
  },
  {
    title: "Self-Care Checklist",
    desc: "Daily practices for wellbeing",
    time: "3 min read",
    icon: Heart,
    iconColor: "text-pink-500",
    iconBg: "bg-pink-50",
    href: "/resources/self-care",
  },
]

export function HelpfulResources() {
  return (
    <Card className="py-6">
      <CardContent className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-2xl font-semibold text-foreground font-sans">Helpful Resources</h3>
          <Link
            href="/activities"
            className="text-sm font-semibold text-primary hover:text-primary/80 transition-colors duration-200"
          >
            Browse All
          </Link>
        </div>

        <div className="flex flex-col gap-4">
          {resources.map((resource) => (
            <Link
              key={resource.title}
              href={resource.href}
              className="flex items-start gap-3 rounded-2xl p-2 -mx-2 transition-all duration-200 hover:bg-accent/50"
            >
              <div className={`flex size-11 shrink-0 items-center justify-center rounded-xl ${resource.iconBg}`}>
                <resource.icon className={`size-5 ${resource.iconColor}`} />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-semibold text-foreground">{resource.title}</p>
                <p className="text-xs text-muted-foreground">{resource.desc}</p>
                <div className="mt-1 flex items-center gap-1 text-xs text-muted-foreground/70">
                  <span>{resource.time}</span>
                  <ExternalLink className="size-3" />
                </div>
              </div>
            </Link>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
