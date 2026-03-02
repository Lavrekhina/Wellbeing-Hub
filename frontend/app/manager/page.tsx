"use client"

import { useState } from "react"
import { Menu } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Sheet,
  SheetContent,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet"
import { Sidebar } from "@/components/dashboard/sidebar"
import { Header } from "@/components/dashboard/header"
import { DepartmentRiskOverview } from "@/components/manager/department-risk-overview"
import { TeamTrendChart } from "@/components/manager/team-trend-chart"
import { AnonymisedBanner } from "@/components/manager/anonymised-banner"

export default function ManagerDashboardPage() {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="flex h-dvh overflow-hidden">
      <Sidebar className="hidden lg:flex" role="manager" />

      <Sheet open={sidebarOpen} onOpenChange={setSidebarOpen}>
        <SheetTrigger asChild>
          <Button
            variant="ghost"
            size="icon"
            className="fixed left-3 top-4 z-40 lg:hidden"
          >
            <Menu className="size-5" />
            <span className="sr-only">Open sidebar</span>
          </Button>
        </SheetTrigger>
        <SheetContent side="left" className="w-64 p-0 glass-sidebar border-r-0">
          <SheetTitle className="sr-only">Navigation Menu</SheetTitle>
          <Sidebar role="manager" />
        </SheetContent>
      </Sheet>

      <div className="flex flex-1 flex-col overflow-hidden">
        <Header />
        <main className="mesh-gradient-bg flex-1 overflow-y-auto p-4 lg:p-8">
          <div className="space-y-8">
            <div>
              <h2 className="text-4xl font-bold text-foreground font-sans">
                Team Overview
              </h2>
              <p className="mt-1 text-sm text-muted-foreground font-medium">
                Anonymised department wellbeing insights
              </p>
            </div>

            <AnonymisedBanner />
            <DepartmentRiskOverview />
            <TeamTrendChart />
          </div>
        </main>
      </div>
    </div>
  )
}