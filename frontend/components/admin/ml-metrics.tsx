"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { getMLMetrics } from "@/lib/api"
import { BrainCircuit, Target, Crosshair } from "lucide-react"

export function MLMetrics() {
  const [metrics, setMetrics] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadMetrics() {
      try {
        const data = await getMLMetrics()
        setMetrics(data)
      } catch (error) {
        console.error("Failed to load ML metrics", error)
      } finally {
        setLoading(false)
      }
    }
    loadMetrics()
  },[])

  if (loading) return <div className="p-8 text-center text-muted-foreground">Loading ML Classifier data...</div>
  if (!metrics) return <div className="p-8 text-center text-destructive">ML Endpoint disabled or unreachable. Ensure EXPOSE_ML_RISK_METRICS=true in backend.</div>

  // Convert decimal to percentage
  const toPct = (val: number) => `${(val * 100).toFixed(1)}%`

  return (
    <div className="space-y-6">
      {/* Top Level ML Scores */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <Card className="border-border/50 shadow-sm">
          <CardContent className="pt-6 flex items-center gap-4">
            <div className="bg-slate-100 p-3 rounded-xl"><Target className="text-slate-600 size-6" /></div>
            <div>
              <p className="text-sm text-muted-foreground font-medium">Overall Accuracy</p>
              <p className="text-3xl font-bold text-slate-800">{toPct(metrics.accuracy)}</p>
            </div>
          </CardContent>
        </Card>
        <Card className="border-border/50 shadow-sm">
          <CardContent className="pt-6 flex items-center gap-4">
            <div className="bg-indigo-50 p-3 rounded-xl"><BrainCircuit className="text-indigo-600 size-6" /></div>
            <div>
              <p className="text-sm text-muted-foreground font-medium">Macro F1 Score</p>
              <p className="text-3xl font-bold text-indigo-800">{toPct(metrics.macro_f1)}</p>
            </div>
          </CardContent>
        </Card>
        <Card className="border-border/50 shadow-sm">
          <CardContent className="pt-6 flex items-center gap-4">
            <div className="bg-teal-50 p-3 rounded-xl"><Crosshair className="text-teal-600 size-6" /></div>
            <div>
              <p className="text-sm text-muted-foreground font-medium">Weighted F1 Score</p>
              <p className="text-3xl font-bold text-teal-800">{toPct(metrics.weighted_f1)}</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Per Class Breakdown */}
      <Card className="border-border/50 shadow-sm">
        <CardHeader className="border-b border-border/50 pb-4">
          <CardTitle className="text-xl font-bold">Risk Classification Performance</CardTitle>
          <CardDescription>Precision and Recall metrics broken down by risk category (Scikit-learn Synthetic Model).</CardDescription>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <TableHeader className="bg-muted/30">
              <TableRow>
                <TableHead>Risk Class</TableHead>
                <TableHead>Precision</TableHead>
                <TableHead>Recall</TableHead>
                <TableHead>F1-Score</TableHead>
                <TableHead className="text-right">Support (Samples)</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {["low", "medium", "high"].map((riskClass) => {
                const data = metrics.per_class[riskClass]
                if (!data) return null
                return (
                  <TableRow key={riskClass}>
                    <TableCell className="font-semibold capitalize">{riskClass}</TableCell>
                    <TableCell>{toPct(data.precision)}</TableCell>
                    <TableCell>{toPct(data.recall)}</TableCell>
                    <TableCell>{toPct(data.f1)}</TableCell>
                    <TableCell className="text-right text-muted-foreground">{data.support}</TableCell>
                  </TableRow>
                )
              })}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}