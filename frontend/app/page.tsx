"use client"

import { useState } from "react"
import { Menu, Heart } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Sheet,
  SheetContent,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet"
import { Sidebar } from "@/components/dashboard/sidebar"
import { Header } from "@/components/dashboard/header"
import { MoodTracker } from "@/components/dashboard/mood-tracker"
import { QuickActions } from "@/components/dashboard/quick-actions"
import { StatCards } from "@/components/dashboard/stat-cards"
import { BurnoutChart } from "@/components/dashboard/burnout-chart"
import { Recommendations } from "@/components/dashboard/recommendations"
import { RecentJournalEntries } from "@/components/dashboard/recent-journal"
import { HelpfulResources } from "@/components/dashboard/helpful-resources"
import { ConsentModal } from "@/components/dashboard/consent-modal"

export default function DashboardPage() {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="flex h-dvh overflow-hidden">

      <ConsentModal />
      
      {/* Desktop Sidebar */}
      <Sidebar className="hidden lg:flex" />

      {/* Mobile Sidebar */}
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
          <Sidebar />
        </SheetContent>
      </Sheet>

      {/* Main Area */}
      <div className="flex flex-1 flex-col overflow-hidden">
        <Header />

        <main className="mesh-gradient-bg flex-1 overflow-y-auto p-4 lg:p-8">
          <div className="space-y-8">
            {/* Welcome Section */}
            <div>
              <h2 className="text-4xl font-bold text-foreground font-sans text-balance">
                Welcome back, Melisa
              </h2>
              <p className="mt-1 text-sm text-muted-foreground font-medium">
                {"Here's your wellness overview for today"}
              </p>
            </div>

            {/* Mood Tracker + Quick Actions */}
            <div className="grid grid-cols-1 gap-5 xl:grid-cols-[1fr_340px]">
              <MoodTracker />
              <QuickActions />
            </div>

            {/* Stat Cards */}
            <StatCards />

            {/* Burnout Chart + Today's Activities */}
            <div className="grid grid-cols-1 gap-5 xl:grid-cols-[1fr_400px]">
              <BurnoutChart />
              <Recommendations />
            </div>

            {/* Journal Entries + Resources */}
            <div className="grid grid-cols-1 gap-5 xl:grid-cols-[1fr_400px]">
              <RecentJournalEntries />
              <HelpfulResources />
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
