"use client"

import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"

const moods = [
  { label: "Great", color: "bg-amber-50", borderColor: "border-amber-200/60", emoji: "\u2600\uFE0F", hoverBg: "hover:bg-amber-100/80", selectedBg: "bg-amber-100" },
  { label: "Good", color: "bg-emerald-50", borderColor: "border-emerald-200/60", emoji: "\uD83D\uDE0A", hoverBg: "hover:bg-emerald-100/80", selectedBg: "bg-emerald-100" },
  { label: "Okay", color: "bg-blue-50", borderColor: "border-blue-200/60", emoji: "\uD83D\uDE10", hoverBg: "hover:bg-blue-100/80", selectedBg: "bg-blue-100" },
  { label: "Low", color: "bg-gray-50", borderColor: "border-gray-200/60", emoji: "\u2601\uFE0F", hoverBg: "hover:bg-gray-100/80", selectedBg: "bg-gray-100" },
  { label: "Struggling", color: "bg-purple-50", borderColor: "border-purple-200/60", emoji: "\uD83C\uDF27\uFE0F", hoverBg: "hover:bg-purple-100/80", selectedBg: "bg-purple-100" },
]

const weekDays = [
  { day: "Mon", color: "bg-emerald-200/70" },
  { day: "Tue", color: "bg-amber-200/70" },
  { day: "Wed", color: "bg-blue-200/70" },
  { day: "Thu", color: "bg-emerald-100/80" },
  { day: "Fri", color: "bg-amber-200/70" },
  { day: "Sat", color: "bg-emerald-100/80" },
  { day: "Sun", color: "bg-gray-100/80" },
]

export function MoodTracker() {
  const [selectedMood, setSelectedMood] = useState<string | null>(null)

  return (
    <Card className="py-6">
      <CardContent className="space-y-5">
        <div>
          <h3 className="text-2xl font-semibold text-foreground font-sans">How are you feeling today?</h3>
          <p className="mt-1 text-sm text-muted-foreground font-medium">Track your mood to identify patterns</p>
        </div>

        {/* Mood Selection - equal width square buttons */}
        <div className="grid grid-cols-5 gap-3">
          {moods.map((mood) => (
            <button
              key={mood.label}
              onClick={() => setSelectedMood(mood.label)}
              className={`flex aspect-square flex-col items-center justify-center gap-2 rounded-2xl border-2 transition-all duration-200 hover:scale-105 hover:shadow-md ${mood.borderColor} ${mood.hoverBg} ${
                selectedMood === mood.label
                  ? `${mood.selectedBg} border-opacity-100 shadow-md scale-105`
                  : mood.color
              }`}
            >
              <span className="text-3xl sm:text-4xl leading-none" role="img" aria-label={mood.label}>
                {mood.emoji}
              </span>
              <span className="text-xs font-semibold text-foreground">{mood.label}</span>
            </button>
          ))}
        </div>

        {/* This Week */}
        <div className="space-y-3">
          <h4 className="text-sm font-bold text-foreground">This Week</h4>
          <div className="flex gap-2">
            {weekDays.map((item) => (
              <div key={item.day} className="flex flex-1 flex-col items-center gap-1.5">
                <div className={`h-16 w-full rounded-xl ${item.color} transition-colors duration-200`} />
                <span className="text-xs text-muted-foreground">{item.day}</span>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
