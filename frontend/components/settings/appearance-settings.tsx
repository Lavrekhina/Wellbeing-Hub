"use client"

import { useState, useEffect } from "react"
import { Laptop } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"

export function AppearanceSettings() {
  const [mounted, setMounted] = useState(false)
  const [reduceMotions, setReduceMotions] = useState(false)

  // Load saved preferences on mount
  useEffect(() => {
    setMounted(true)
    const savedMotion = localStorage.getItem("reduce-motions") === "true"
    setReduceMotions(savedMotion)
    if (savedMotion) {
      document.documentElement.classList.add("reduce-motion")
    }
  },[])

  // Handle the motion toggle
  const handleMotionToggle = (checked: boolean) => {
    setReduceMotions(checked)
    localStorage.setItem("reduce-motions", String(checked))
    if (checked) {
      document.documentElement.classList.add("reduce-motion")
    } else {
      document.documentElement.classList.remove("reduce-motion")
    }
  }

  if (!mounted) return null

  return (
    <div className="space-y-6">
      <Card className="border-border/50 shadow-sm">
        <CardHeader className="border-b border-border/50 pb-4">
          <CardTitle className="text-xl">Theme Preferences</CardTitle>
          <CardDescription>Customise how the Wellbeing Hub looks on your device.</CardDescription>
        </CardHeader>
        <CardContent className="pt-6">
          
          {/* Accessibility Toggle Only */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-muted p-2 rounded-lg">
                <Laptop className="size-5 text-slate-500" />
              </div>
              <div className="space-y-0.5">
                <Label className="text-base font-semibold">Reduce Animations</Label>
                <p className="text-xs text-muted-foreground">
                  Minimise UI motion and hover effects across the dashboard.
                </p>
              </div>
            </div>
            <Switch 
              checked={reduceMotions} 
              onCheckedChange={handleMotionToggle} 
            />
          </div>

        </CardContent>
      </Card>
    </div>
  )
}