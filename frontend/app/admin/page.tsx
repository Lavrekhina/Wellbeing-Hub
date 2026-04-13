"use client"

import { Sidebar } from "@/components/dashboard/sidebar"
import { Header } from "@/components/dashboard/header"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { UsersTable } from "@/components/admin/users-table"
import { DepartmentsTable } from "@/components/admin/departments-table"
import { ShieldAlert } from "lucide-react"

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
                  Manage users, departments, and system access levels
                </p>
              </div>
            </div>

            {/* Tabs for Database Viewer */}
            <Tabs defaultValue="users" className="w-full space-y-6">
              <TabsList className="bg-card border border-border/50 p-1 rounded-xl">
                <TabsTrigger value="users" className="rounded-lg px-6">User Management</TabsTrigger>
                <TabsTrigger value="departments" className="rounded-lg px-6">Departments</TabsTrigger>
              </TabsList>

              <TabsContent value="users" className="outline-none">
                <UsersTable />
              </TabsContent>

              <TabsContent value="departments" className="outline-none">
                <DepartmentsTable />
              </TabsContent>
            </Tabs>

          </div>
        </main>
      </div>
    </div>
  )
}