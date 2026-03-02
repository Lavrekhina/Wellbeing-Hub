"use client"

import { useState } from "react"
import { ShieldCheck, X } from "lucide-react"
import { Button } from "@/components/ui/button"

export function ConsentModal() {
  const [open, setOpen] = useState(true)

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
      <div className="relative mx-4 w-full max-w-lg rounded-3xl bg-white p-8 shadow-2xl">
        
        {/* Icon */}
        <div className="mb-5 flex size-14 items-center justify-center rounded-2xl bg-violet-50">
          <ShieldCheck className="size-7 text-violet-600" />
        </div>

        {/* Title */}
        <h2 className="text-2xl font-bold text-foreground">
          Your Data, Your Control
        </h2>
        <p className="mt-2 text-sm text-muted-foreground">
          Before you begin, please review how the Wellbeing Hub uses your data.
        </p>

        {/* What we collect */}
        <div className="mt-6 space-y-2">
          <p className="text-sm font-semibold text-foreground">What we collect:</p>
          <ul className="space-y-1.5 text-sm text-muted-foreground">
            <li className="flex items-start gap-2">
              <span className="mt-1 size-1.5 shrink-0 rounded-full bg-violet-400" />
              Mood check-ins and wellbeing survey responses
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-1 size-1.5 shrink-0 rounded-full bg-violet-400" />
              Journal entries for AI sentiment analysis
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-1 size-1.5 shrink-0 rounded-full bg-violet-400" />
              Work pattern data (hours, activity scores)
            </li>
          </ul>
        </div>

        {/* Your rights */}
        <div className="mt-5 space-y-2">
          <p className="text-sm font-semibold text-foreground">Your rights under GDPR:</p>
          <ul className="space-y-1.5 text-sm text-muted-foreground">
            <li className="flex items-start gap-2">
              <span className="mt-1 size-1.5 shrink-0 rounded-full bg-emerald-400" />
              All data is anonymised before being shared with managers
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-1 size-1.5 shrink-0 rounded-full bg-emerald-400" />
              You can withdraw consent and delete your data at any time via Settings
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-1 size-1.5 shrink-0 rounded-full bg-emerald-400" />
              AI outputs are used to support you, never for employment decisions
            </li>
          </ul>
        </div>

        {/* Buttons */}
        <div className="mt-8 flex flex-col gap-3 sm:flex-row">
          <Button
            className="gradient-primary flex-1 rounded-2xl py-3 text-sm font-semibold text-white shadow-md"
            onClick={() => setOpen(false)}
          >
            I Accept
          </Button>
          <Button
            variant="outline"
            className="flex-1 rounded-2xl py-3 text-sm font-semibold"
            onClick={() => setOpen(false)}
          >
            Decline
          </Button>
        </div>

        <p className="mt-4 text-center text-xs text-muted-foreground">
          You can review this agreement at any time in Settings → Privacy
        </p>
      </div>
    </div>
  )
}