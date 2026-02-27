"use client"

import Link from "next/link"
import { Search, Bell } from "lucide-react"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"

export function Header() {
  return (
    <header className="glass-sidebar flex h-18 shrink-0 items-center justify-between gap-4 border-b border-sidebar-border px-4 lg:px-8">
      {/* Search */}
      <div className="relative flex-1 max-w-lg">
        <Search className="absolute left-4 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
        <input
          type="search"
          placeholder="Search activities, journal entries..."
          className="h-11 w-full rounded-2xl border border-input bg-card/60 pl-11 pr-4 text-sm text-foreground placeholder:text-muted-foreground outline-none backdrop-blur-sm transition-all duration-200 focus:border-primary/40 focus:ring-4 focus:ring-primary/10 focus:bg-card"
        />
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-4">
        <Link href="/notifications">
          <Button variant="ghost" size="icon" className="relative rounded-2xl hover:bg-secondary">
            <Bell className="size-5 text-muted-foreground" />
            <span className="absolute right-2 top-2 size-2 rounded-full bg-destructive ring-2 ring-card" />
            <span className="sr-only">Notifications</span>
          </Button>
        </Link>

        <Link href="/profile" className="flex items-center gap-3">
          <div className="hidden text-right sm:block">
            <p className="text-sm font-semibold text-foreground">Melisa Sistek</p>
            <p className="text-xs text-muted-foreground">Member since Jan 2024</p>
          </div>
          <Avatar className="size-10 ring-2 ring-primary/20 ring-offset-2 ring-offset-card">
            <AvatarFallback className="gradient-primary text-sm font-semibold text-primary-foreground">
              MS
            </AvatarFallback>
          </Avatar>
        </Link>
      </div>
    </header>
  )
}
