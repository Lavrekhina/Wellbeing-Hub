"use client"

import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { submitCheckin } from "@/lib/api"

const HARDCODED_USER_ID = 1
const HARDCODED_SURVEY_ID = 1
const HARDCODED_DEPARTMENT_ID = 1

const moods = [
  { label: "Great", value: 0.0, color: "bg-amber-50", borderColor: "border-amber-200/60", emoji: "\u2600\uFE0F", hoverBg: "hover:bg-amber-100/80", selectedBg: "bg-amber-100" },
  { label: "Good", value: 1.25, color: "bg-emerald-50", borderColor: "border-emerald-200/60", emoji: "\uD83D\uDE0A", hoverBg: "hover:bg-emerald-100/80", selectedBg: "bg-emerald-100" },
  { label: "Okay", value: 2.5, color: "bg-blue-50", borderColor: "border-blue-200/60", emoji: "\uD83D\uDE10", hoverBg: "hover:bg-blue-100/80", selectedBg: "bg-blue-100" },
  { label: "Low", value: 3.75, color: "bg-gray-50", borderColor: "border-gray-200/60", emoji: "\u2601\uFE0F", hoverBg: "hover:bg-gray-100/80", selectedBg: "bg-gray-100" },
  { label: "Struggling", value: 5.0, color: "bg-purple-50", borderColor: "border-purple-200/60", emoji: "\uD83C\uDF27\uFE0F", hoverBg: "hover:bg-purple-100/80", selectedBg: "bg-purple-100" },
]

export function MoodTracker() {
  const [selectedMood, setSelectedMood] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)
  const [submitted, setSubmitted] = useState(false)

  async function handleMoodSelect(label: string, value: number) {
    setSelectedMood(label)
    setSubmitting(true)
    try {
      await submitCheckin(
        HARDCODED_USER_ID,
        HARDCODED_SURVEY_ID,
        HARDCODED_DEPARTMENT_ID,
        true,
        [{ question_id: 1, answer_value: value }]
      )
      setSubmitted(true)
    } catch {
      // silent fail for now
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Card className="py-6">
      <CardContent className="space-y-5">
        <div>
          <h3 className="text-2xl font-semibold text-foreground font-sans">
            How are you feeling today?
          </h3>
          <p className="mt-1 text-sm text-muted-foreground font-medium">
            Track your mood to identify patterns
          </p>
        </div>

        <div className="grid grid-cols-5 gap-3">
          {moods.map((mood) => (
            <button
              key={mood.label}
              onClick={() => handleMoodSelect(mood.label, mood.value)}
              disabled={submitting}
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

        {submitted && (
          <p className="text-xs font-medium text-emerald-600">
            ✓ Check-in saved successfully
          </p>
        )}

        {submitting && (
          <p className="text-xs text-muted-foreground">Saving...</p>
        )}
      </CardContent>
    </Card>
  )
}