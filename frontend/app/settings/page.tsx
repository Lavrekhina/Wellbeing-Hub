"use client"

import { Sidebar } from "@/components/dashboard/sidebar"
import { Header } from "@/components/dashboard/header"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { AppearanceSettings } from "@/components/settings/appearance-settings"
import { PrivacySettings } from "@/components/settings/privacy-settings"
import { Settings as SettingsIcon } from "lucide-react"

export default function SettingsPage() {
  return (
    <div className="flex h-dvh overflow-hidden">
      <Sidebar className="hidden lg:flex" />

      <div className="flex flex-1 flex-col overflow-hidden">
        <Header />
        
        <main className="mesh-gradient-bg flex-1 overflow-y-auto p-4 lg:p-8">
          <div className="space-y-8 max-w-5xl mx-auto">
            {/* Header */}
            <div className="flex items-center gap-3">
              <div className="bg-slate-800 p-3 rounded-2xl shadow-lg">
                <SettingsIcon className="size-6 text-white" />
              </div>
              <div>
                <h2 className="text-3xl font-bold text-foreground font-sans">
                  Settings & Preferences
                </h2>
                <p className="mt-1 text-sm text-muted-foreground font-medium">
                  Manage your account, appearance, and privacy controls
                </p>
              </div>
            </div>

            {/* Settings Tabs */}
            <Tabs defaultValue="appearance" className="w-full space-y-6">
              <TabsList className="bg-card border border-border/50 p-1 rounded-xl">
                <TabsTrigger value="appearance" className="rounded-lg px-6">Appearance</TabsTrigger>
                <TabsTrigger value="privacy" className="rounded-lg px-6">Privacy & Data</TabsTrigger>
              </TabsList>

              <TabsContent value="appearance" className="outline-none">
                <AppearanceSettings />
              </TabsContent>

              <TabsContent value="privacy" className="outline-none">
                <PrivacySettings />
              </TabsContent>
            </Tabs>
          </div>
        </main>
      </div>
    </div>
  )
}