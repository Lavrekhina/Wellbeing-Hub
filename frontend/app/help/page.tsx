"use client"

import { Sidebar } from "@/components/dashboard/sidebar"
import { Header } from "@/components/dashboard/header"
import { HelpContent } from "@/components/help/help-content"
import { BookOpen, LifeBuoy } from "lucide-react"

export default function HelpPage() {
  return (
    <div className="flex h-dvh overflow-hidden">
      <Sidebar className="hidden lg:flex" />

      <div className="flex flex-1 flex-col overflow-hidden">
        <Header />
        
        <main className="mesh-gradient-bg flex-1 overflow-y-auto p-4 lg:p-8">
          <div className="max-w-4xl mx-auto space-y-8">
            {/* Header Section */}
            <div className="flex items-center gap-4">
              <div className="gradient-primary p-3 rounded-2xl shadow-lg shadow-primary/20">
                <LifeBuoy className="size-6 text-white" />
              </div>
              <div>
                <h2 className="text-4xl font-bold text-foreground font-sans">
                  Help & Support
                </h2>
                <p className="mt-1 text-sm text-muted-foreground font-medium">
                  Learn about our technology, privacy standards, and how to use the hub
                </p>
              </div>
            </div>

            {/* Main FAQ/Transparency Component */}
            <HelpContent />

            {/* Contact Footer */}
            <div className="rounded-3xl border border-border/50 bg-card p-8 ambient-shadow text-center space-y-4">
              <h3 className="text-xl font-bold text-foreground">Still have questions?</h3>
              <p className="text-sm text-muted-foreground max-w-md mx-auto">
                If you need further assistance regarding your data or the platform's features, please contact your internal HR wellbeing representative.
              </p>
              <button className="text-primary font-semibold hover:underline text-sm">
                View Privacy Policy
              </button>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}