"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import {
  LayoutDashboard,
  Activity,
  BookOpen,
  Heart,
  Settings,
  HelpCircle,
  ShieldAlert,
  BarChart3
} from "lucide-react"

// Employee gets the core wellbeing loop
const employeeNavItems =[
  { label: "Dashboard", href: "/", icon: LayoutDashboard },
  { label: "Activities", href: "/activities", icon: Activity },
  { label: "Mindful Journal", href: "/journal", icon: BookOpen },
]

// Manager gets just their anonymized team view
const managerNavItems =[
  { label: "Team Wellbeing", href: "/manager", icon: BarChart3 },
]

// HR gets the global org view
const hrNavItems =[
  { label: "Organization Overview", href: "/hr", icon: LayoutDashboard },
]

// Admin gets the system and ML metrics
const adminNavItems =[
  { label: "Admin Console", href: "/admin", icon: ShieldAlert },
]

// Bottom items stay the same for everyone (Privacy and Help)
const bottomItems =[
  { label: "Settings", href: "/settings", icon: Settings },
  { label: "Help", href: "/help", icon: HelpCircle },
]

export function Sidebar({ className, role = "employee" }: { className?: string, role?: string }) {
  const pathname = usePathname()

  let navItems = employeeNavItems
  if (role === "manager") navItems = managerNavItems
  if (role === "hr") navItems = hrNavItems
  if (role === "admin") navItems = adminNavItems

  return (
    <aside
      className={cn(
        "glass-sidebar flex h-full w-64 flex-col border-r border-sidebar-border",
        className
      )}
    >
      {/* Logo */}
      <div className="flex items-center gap-3 px-5 py-7">
        <div className="gradient-primary flex size-11 items-center justify-center rounded-2xl shadow-lg shadow-primary/25">
          <Heart className="size-5 text-primary-foreground" fill="currentColor" />
        </div>
        <div>
          <h1 className="text-base font-bold text-sidebar-foreground tracking-tight">Wellbeing Hub</h1>
          <p className="text-xs text-sidebar-foreground/60">Your wellness journey</p>
        </div>
      </div>

      {/* Main Navigation */}
      <nav className="flex flex-1 flex-col gap-1.5 px-3">
        {navItems.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.label}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-full px-4 py-2.5 text-sm font-medium transition-all duration-200",
                isActive
                  ? "gradient-primary text-primary-foreground shadow-md shadow-primary/20"
                  : "text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground hover:rounded-full"
              )}
            >
              <item.icon className="size-4.5" />
              {item.label}
            </Link>
          )
        })}
      </nav>

      {/* Bottom Navigation */}
      <div className="flex flex-col gap-1.5 border-t border-sidebar-border px-3 py-5">
        {bottomItems.map((item) => (
          <Link
            key={item.label}
            href={item.href}
            className="flex items-center gap-3 rounded-full px-4 py-2.5 text-sm font-medium text-sidebar-foreground transition-all duration-200 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
          >
            <item.icon className="size-4.5" />
            {item.label}
          </Link>
        ))}
      </div>
    </aside>
  )
}
