"use client"

import { useEffect, useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Sparkles, AlertCircle } from "lucide-react"
import { getRecommendations } from "@/lib/api"

const HARDCODED_USER_ID = 1

export function Recommendations() {
  const [recommendations, setRecommendations] = useState<string[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    async function fetchRecommendations() {
      try {
        const data = await getRecommendations(HARDCODED_USER_ID)
        setRecommendations(data.recommendations)
      } catch {
        setError(true)
      } finally {
        setLoading(false)
      }
    }
    fetchRecommendations()
  }, [])

  return (
    <Card className="py-6">
      <CardContent className="space-y-4">
        <div className="flex items-center gap-2">
          <div className="flex size-8 items-center justify-center rounded-xl bg-violet-50">
            <Sparkles className="size-4 text-violet-600" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-foreground">
              AI Recommendations
            </h3>
            <p className="text-xs text-muted-foreground">
              Based on your latest check-in
            </p>
          </div>
        </div>

        {loading && (
          <div className="space-y-2">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="h-4 w-full animate-pulse rounded-full bg-muted"
              />
            ))}
          </div>
        )}

        {error && (
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <AlertCircle className="size-4" />
            <p>Could not load recommendations right now.</p>
          </div>
        )}

        {!loading && !error && recommendations.length === 0 && (
          <p className="text-sm text-muted-foreground">
            Complete a check-in to receive personalised recommendations.
          </p>
        )}

        {!loading && !error && recommendations.length > 0 && (
          <ul className="space-y-3">
            {recommendations.map((rec, index) => (
              <li key={index} className="flex items-start gap-3">
                <span className="mt-1.5 size-1.5 shrink-0 rounded-full bg-violet-400" />
                <p className="text-sm text-foreground leading-relaxed">{rec}</p>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  )
}