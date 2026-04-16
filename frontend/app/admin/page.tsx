"use client"

import { Sidebar } from "@/components/dashboard/sidebar"
import { Header } from "@/components/dashboard/header"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ShieldAlert } from "lucide-react"
import { AdminOverview } from "@/components/admin/admin-overview"
import { MLMetrics } from "@/components/admin/ml-metrics"

export default function AdminDashboardPage() {
  return (
    <div className="flex h-dvh overflow-hidden">
      <Sidebar className="hidden lg:flex" role="admin" />

      <div className="flex flex-1 flex-col overflow-hidden">
        <Header />
        
        <main className="mesh-gradient-bg flex-1 overflow-y-auto p-4 lg:p-8">
          <div className="space-y-8 max-w-7xl mx-auto">
            {/* Header */}
            <div className="flex items-center gap-3">
              <div className="bg-slate-800 p-3 rounded-2xl shadow-lg">
                <ShieldAlert className="size-6 text-white" />
              </div>
              <div>
                <h2 className="text-3xl font-bold text-foreground font-sans">
                  System Administration
                </h2>
                <p className="mt-1 text-sm text-muted-foreground font-medium">
                  Monitor system health, live assessments, and Machine Learning performance
                </p>
              </div>
            </div>

            {/* Tabs */}
            <Tabs defaultValue="overview" className="w-full space-y-6">
              <TabsList className="bg-card border border-border/50 p-1 rounded-xl">
                <TabsTrigger value="overview" className="rounded-lg px-6">System Overview</TabsTrigger>
                <TabsTrigger value="ml-metrics" className="rounded-lg px-6">ML Classifier Metrics</TabsTrigger>
              </TabsList>

              <TabsContent value="overview" className="outline-none">
                <AdminOverview />
              </TabsContent>

              <TabsContent value="ml-metrics" className="outline-none">
                <MLMetrics />
              </TabsContent>
            </Tabs>

          </div>
        </main>
      </div>
    </div>
  )
}