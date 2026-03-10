"use client"

import { useState, useEffect } from "react"
import { BarChart3, Activity } from "lucide-react"
import { Sidebar } from "@/components/dashboard/sidebar"
import { Header } from "@/components/dashboard/header"
import { AnonymisedBanner } from "@/components/manager/anonymised-banner"
import { OrgRiskSummaryCards } from "@/components/hr/org-risk-summary-cards"
import { DepartmentComparisonList } from "@/components/hr/department-comparison-list"
import { OrgTrendChart } from "@/components/hr/org-trend-chart"
import { getDepartmentRiskSummary } from "@/lib/api"

//realistic dummy data for the demo fallback
const fallbackOrgData = {
  min_group_size: 3,
  excluded_departments: 2,
  departments: [
    {
      department_label: "Engineering",
      response_count: 24,
      avg_risk_score: 32,
      high_risk_ratio: 0.08,
      risk_level_breakdown: { low: 18, medium: 4, high: 2 }
    },
    {
      department_label: "Sales & Marketing",
      response_count: 18,
      avg_risk_score: 54,
      high_risk_ratio: 0.22,
      risk_level_breakdown: { low: 6, medium: 8, high: 4 }
    },
    {
      department_label: "Customer Support",
      response_count: 15,
      avg_risk_score: 41,
      high_risk_ratio: 0.13,
      risk_level_breakdown: { low: 8, medium: 5, high: 2 }
    }
  ]
}

export default function HRDashboardPage() {
  const [loading, setLoading] = useState(true)
  const [orgData, setOrgData] = useState<any>(fallbackOrgData)
  const [isRealData, setIsRealData] = useState(false)

  useEffect(() => {
    async function fetchData() {
      try {
        const data = await getDepartmentRiskSummary(3)
        if (data && data.departments && data.departments.length > 0) {
          setOrgData(data)
          setIsRealData(true)
        }
      } catch (error) {
        console.log("Using fallback data for HR demo")
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  return (
    <div className="flex h-dvh overflow-hidden">
      <Sidebar className="hidden lg:flex" role="hr" />

      <div className="flex flex-1 flex-col overflow-hidden">
        <Header />
        
        <main className="mesh-gradient-bg flex-1 overflow-y-auto p-4 lg:p-8">
          <div className="space-y-8">
            <div className="flex items-start justify-between">
              <div>
                <h2 className="text-4xl font-bold text-foreground font-sans">
                  Organization Overview
                </h2>
                <p className="mt-1 text-sm text-muted-foreground font-medium">
                  High-level wellbeing aggregates across all departments
                </p>
              </div>
              {!isRealData && !loading && (
                <span className="text-[10px] font-bold uppercase tracking-widest text-amber-600 bg-amber-50 border border-amber-200 px-2 py-1 rounded-md">
                  Demo Mode: Sample Data
                </span>
              )}
            </div>

            <AnonymisedBanner />

            <OrgRiskSummaryCards data={orgData} loading={loading} />

            {/* Added Organizational Trend Chart */}
            <OrgTrendChart isRealData={isRealData} />

            <div className="space-y-4">
              <div className="flex items-center gap-2">
                <BarChart3 className="size-5 text-primary" />
                <h3 className="text-2xl font-semibold text-foreground font-sans">
                  Department Analysis
                </h3>
              </div>
              <DepartmentComparisonList departments={orgData?.departments || []} loading={loading} />
            </div>
            
            <div className="rounded-2xl border border-border/40 bg-card/40 p-6 backdrop-blur-sm">
               <p className="text-xs text-muted-foreground leading-relaxed">
                <strong>Data Privacy Policy:</strong> Organization-wide reporting enforces a minimum 
                group size of {orgData?.min_group_size || 3}. This protects employee anonymity by 
                automatically redacting specific metrics for smaller cohorts.
               </p>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}