"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { getAdminOverview, getAdminRecentAssessments } from "@/lib/api"
import { Activity, FileText, CheckCircle2 } from "lucide-react"

export function AdminOverview() {
  const [overview, setOverview] = useState<any>(null)
  const [assessments, setAssessments] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadData() {
      try {
        const [overviewData, recentData] = await Promise.all([
          getAdminOverview(),
          getAdminRecentAssessments(15) // Fetch latest 15
        ])
        setOverview(overviewData)
        setAssessments(recentData.items ||[])
      } catch (error) {
        console.error("Failed to load admin data", error)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  },[])

  if (loading) return <div className="p-8 text-center text-muted-foreground">Loading secure system data...</div>

  return (
    <div className="space-y-6">
      {/* High Level Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <Card className="border-border/50 shadow-sm">
          <CardContent className="pt-6 flex items-center gap-4">
            <div className="bg-blue-50 p-3 rounded-xl"><FileText className="text-blue-600 size-6" /></div>
            <div>
              <p className="text-sm text-muted-foreground font-medium">Total Responses</p>
              <p className="text-3xl font-bold">{overview?.total_survey_responses || 0}</p>
            </div>
          </CardContent>
        </Card>
        <Card className="border-border/50 shadow-sm">
          <CardContent className="pt-6 flex items-center gap-4">
            <div className="bg-violet-50 p-3 rounded-xl"><Activity className="text-violet-600 size-6" /></div>
            <div>
              <p className="text-sm text-muted-foreground font-medium">Total Assessments</p>
              <p className="text-3xl font-bold">{overview?.total_risk_assessments || 0}</p>
            </div>
          </CardContent>
        </Card>
        <Card className="border-border/50 shadow-sm">
          <CardContent className="pt-6 flex items-center gap-4">
            <div className="bg-emerald-50 p-3 rounded-xl"><CheckCircle2 className="text-emerald-600 size-6" /></div>
            <div>
              <p className="text-sm text-muted-foreground font-medium">Recommendations Generated</p>
              <p className="text-3xl font-bold">{overview?.total_recommendations || 0}</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Assessments Table */}
      <Card className="border-border/50 shadow-sm">
        <CardHeader className="border-b border-border/50 pb-4 flex flex-row items-center justify-between">
          <CardTitle className="text-xl font-bold">Recent Risk Assessments</CardTitle>
          <div className="flex gap-2">
            <Badge variant="outline" className="text-red-600 bg-red-50 border-red-200">High Risk: {overview?.latest_assessment_risk_breakdown?.high || 0}</Badge>
            <Badge variant="outline" className="text-amber-600 bg-amber-50 border-amber-200">Med Risk: {overview?.latest_assessment_risk_breakdown?.medium || 0}</Badge>
            <Badge variant="outline" className="text-emerald-600 bg-emerald-50 border-emerald-200">Low Risk: {overview?.latest_assessment_risk_breakdown?.low || 0}</Badge>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <TableHeader className="bg-muted/30">
              <TableRow>
                <TableHead className="w-[120px]">ID</TableHead>
                <TableHead>User ID</TableHead>
                <TableHead>Risk Score</TableHead>
                <TableHead>Risk Level</TableHead>
                <TableHead className="text-right">Timestamp</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {assessments.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} className="text-center py-8 text-muted-foreground">
                    No recent assessments found.
                  </TableCell>
                </TableRow>
              ) : assessments.map((assessment) => (
                <TableRow key={assessment.assessment_id}>
                  <TableCell className="font-medium text-muted-foreground">#{assessment.assessment_id}</TableCell>
                  <TableCell>User {assessment.user_id}</TableCell>
                  <TableCell className="font-semibold">{assessment.risk_score}%</TableCell>
                  <TableCell>
                    <Badge className={
                      assessment.risk_level === "high" ? "bg-red-100 text-red-700" :
                      assessment.risk_level === "medium" ? "bg-amber-100 text-amber-700" :
                      "bg-emerald-100 text-emerald-700"
                    }>
                      {assessment.risk_level}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right text-xs text-muted-foreground">
                    {new Date(assessment.generated_at).toLocaleString()}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}