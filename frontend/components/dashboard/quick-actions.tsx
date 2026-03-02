import Link from "next/link"
import { Card, CardContent } from "@/components/ui/card"
import { Wind, BookOpen, Headphones, Phone } from "lucide-react"

const actions = [
  { label: "Breathing", desc: "5 min exercise", icon: Wind, color: "text-teal-600", bg: "bg-teal-50", href: "/activities/breathing" },
  { label: "Journal", desc: "Write thoughts", icon: BookOpen, color: "text-primary", bg: "bg-secondary", href: "/journal/new" },
  { label: "Meditate", desc: "Guided session", icon: Headphones, color: "text-pink-600", bg: "bg-pink-50", href: "/activities/meditate" },
  { label: "Support", desc: "Talk to someone", icon: Phone, color: "text-emerald-600", bg: "bg-emerald-50", href: "/support" },
]

export function QuickActions() {
  return (
    <Card className="py-6">
      <CardContent className="space-y-4">
        <h3 className="text-2xl font-semibold text-foreground font-sans">Quick Actions</h3>
        <div className="flex flex-col gap-3">
          {actions.map((action) => (
            <Link
              key={action.label}
              href={action.href}
              className="flex items-center gap-3 rounded-2xl border border-border/50 p-3.5 text-left transition-all duration-200 hover:bg-accent/60 hover:shadow-sm hover:-translate-y-0.5"
            >
              <div className={`flex size-11 shrink-0 items-center justify-center rounded-xl ${action.bg}`}>
                <action.icon className={`size-5 ${action.color}`} />
              </div>
              <div>
                <p className="text-sm font-semibold text-foreground">{action.label}</p>
                <p className="text-xs text-muted-foreground">{action.desc}</p>
              </div>
            </Link>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
