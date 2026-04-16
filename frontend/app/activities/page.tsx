"use client"

import { Sidebar } from "@/components/dashboard/sidebar"
import { Header } from "@/components/dashboard/header"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Wind, Headphones, BookOpen, Dumbbell, PlayCircle } from "lucide-react"

const activities =[
  { title: "Box Breathing", dur: "5 min", cat: "Relaxation", icon: Wind, color: "text-blue-500", bg: "bg-blue-50" },
  { title: "Guided Meditation", dur: "10 min", cat: "Mindfulness", icon: Headphones, color: "text-purple-500", bg: "bg-purple-50" },
  { title: "Digital Detox Guide", dur: "3 min read", cat: "Productivity", icon: BookOpen, color: "text-amber-500", bg: "bg-amber-50" },
  { title: "Desk Yoga", dur: "8 min", cat: "Physical", icon: Dumbbell, color: "text-emerald-500", bg: "bg-emerald-50" },
  { title: "Sleep Hygiene", dur: "4 min read", cat: "Recovery", icon: BookOpen, color: "text-indigo-500", bg: "bg-indigo-50" },
  { title: "Focus Sounds", dur: "45 min", cat: "Focus", icon: Headphones, color: "text-rose-500", bg: "bg-rose-50" },
]

export default function ActivitiesPage() {
  return (
    <div className="flex h-dvh overflow-hidden">
      <Sidebar className="hidden lg:flex" />
      <div className="flex flex-1 flex-col overflow-hidden">
        <Header />
        <main className="mesh-gradient-bg flex-1 overflow-y-auto p-4 lg:p-8">
          <div className="max-w-6xl mx-auto space-y-8">
            <div>
              <h2 className="text-4xl font-bold text-foreground font-sans">Wellbeing Activities</h2>
              <p className="mt-1 text-sm text-muted-foreground font-medium">Personalised resources to help you build mental resilience</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {activities.map((item) => (
                <Card key={item.title} className="ambient-shadow border-none hover:-translate-y-1 transition-transform cursor-pointer group bg-card">
                  <CardContent className="pt-6 space-y-4">
                    <div className={`size-12 rounded-2xl ${item.bg} flex items-center justify-center`}>
                      <item.icon className={`size-6 ${item.color}`} />
                    </div>
                    <div>
                      <Badge variant="secondary" className="mb-3">{item.cat}</Badge>
                      <h3 className="font-bold text-xl text-foreground">{item.title}</h3>
                      <p className="text-sm text-muted-foreground mt-1">{item.dur}</p>
                    </div>
                    <div className="flex items-center gap-2 text-sm font-semibold text-primary opacity-0 group-hover:opacity-100 transition-opacity pt-2">
                      <PlayCircle className="size-5" /> Start Activity
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}