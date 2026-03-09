"use client"

import { useState } from "react"
import { Heart, Eye, EyeOff } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function LoginPage() {
  const [showPassword, setShowPassword] = useState(false)
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  return (
    <div className="mesh-gradient-bg flex min-h-dvh items-center justify-center p-4">
      <div className="w-full max-w-md">

        {/* Logo */}
        <div className="mb-8 flex flex-col items-center gap-3">
          <div className="gradient-primary flex size-16 items-center justify-center rounded-3xl shadow-lg shadow-primary/25">
            <Heart className="size-8 text-white" fill="currentColor" />
          </div>
          <div className="text-center">
            <h1 className="text-2xl font-bold text-foreground">Wellbeing Hub</h1>
            <p className="text-sm text-muted-foreground">Your wellness journey</p>
          </div>
        </div>

        {/* Card */}
        <div className="ambient-shadow rounded-3xl bg-card p-8">
          <div className="mb-6">
            <h2 className="text-xl font-bold text-foreground">Welcome back</h2>
            <p className="mt-1 text-sm text-muted-foreground">
              Sign in to your account to continue
            </p>
          </div>

          <div className="space-y-5">
            {/* Email */}
            <div className="space-y-2">
              <Label htmlFor="email" className="text-sm font-medium">
                Email address
              </Label>
              <Input
                id="email"
                type="email"
                placeholder="you@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="rounded-xl border-border/50 bg-background/60 py-5"
              />
            </div>

            {/* Password */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label htmlFor="password" className="text-sm font-medium">
                  Password
                </Label>
                <button
                  type="button"
                  className="text-xs font-medium text-primary hover:underline"
                >
                  Forgot password?
                </button>
              </div>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="rounded-xl border-border/50 bg-background/60 py-5 pr-10"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                >
                  {showPassword
                    ? <EyeOff className="size-4" />
                    : <Eye className="size-4" />
                  }
                </button>
              </div>
            </div>

            {/* Submit */}
            <Button
              className="gradient-primary w-full rounded-xl py-5 text-sm font-semibold text-white shadow-md shadow-primary/20"
            >
              Sign in
            </Button>
          </div>

          {/* Footer note */}
          <p className="mt-6 text-center text-xs text-muted-foreground">
            Don't have an account? Contact your administrator.
          </p>
        </div>

        <p className="mt-6 text-center text-xs text-muted-foreground">
          Protected by GDPR-compliant data handling
        </p>
      </div>
    </div>
  )
}