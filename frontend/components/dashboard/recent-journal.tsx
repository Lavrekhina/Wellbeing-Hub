import Link from "next/link"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { BookOpen, MoreVertical } from "lucide-react"

const entries = [
  {
    title: "Project deadline reflections",
    excerpt:
      "Successfully completed the Q1 presentation. The team collaboration was excellent, though I felt the pressure building up. Need to delegate more next...",
    date: "Feb 9, 2026 \u00b7 9:15 AM",
    dotColor: "bg-amber-400",
    href: "/journal/1",
  },
  {
    title: "Team meeting insights",
    excerpt:
      "Today\u2019s standup went smoothly. I appreciate how supportive the team is. Feeling a bit overwhelmed with the sprint workload, but taking breaks helps...",
    date: "Feb 8, 2026 \u00b7 8:30 PM",
    dotColor: "bg-blue-400",
    href: "/journal/2",
  },
  {
    title: "Work-life balance check",
    excerpt:
      "Managed to leave work on time today. The boundary I set with email notifications after 6 PM is really helping reduce evening stress. Small wins matter...",
    date: "Feb 7, 2026 \u00b7 7:00 PM",
    dotColor: "bg-amber-300",
    href: "/journal/3",
  },
]

export function RecentJournalEntries() {
  return (
    <Card className="py-6">
      <CardContent className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BookOpen className="size-5 text-primary" />
            <h3 className="text-2xl font-semibold text-foreground font-sans">Recent Journal Entries</h3>
          </div>
          <Link
            href="/journal/new"
            className="text-sm font-semibold text-primary hover:text-primary/80 transition-colors duration-200"
          >
            New Entry
          </Link>
        </div>

        <div className="flex flex-col gap-4">
          {entries.map((entry) => (
            <Link
              key={entry.title}
              href={entry.href}
              className="block space-y-2 rounded-2xl border border-border/40 p-4 transition-all duration-200 hover:bg-accent/40 hover:shadow-sm hover:-translate-y-0.5"
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2">
                  <div className={`size-2.5 shrink-0 rounded-full ${entry.dotColor}`} />
                  <h4 className="text-sm font-semibold text-foreground">{entry.title}</h4>
                </div>
                <Button variant="ghost" size="icon" className="shrink-0 size-7 text-muted-foreground rounded-xl" tabIndex={-1}>
                  <MoreVertical className="size-4" />
                </Button>
              </div>
              <p className="text-sm leading-relaxed text-muted-foreground">
                {entry.excerpt}
              </p>
              <p className="text-xs text-muted-foreground/70">{entry.date}</p>
            </Link>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
