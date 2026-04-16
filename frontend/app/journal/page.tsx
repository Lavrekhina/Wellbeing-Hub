"use client"

import { useState } from "react"
import { Sidebar } from "@/components/dashboard/sidebar"
import { Header } from "@/components/dashboard/header"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Sparkles, History, Save } from "lucide-react"

export default function JournalPage() {
  const [entry, setEntry] = useState("")
  const [isSaved, setIsSaved] = useState(false)

  const handleSave = () => {
    setIsSaved(true)
    setTimeout(() => setIsSaved(false), 3000)
    setEntry("") // Clear the text area after "saving"
  }

  return (
    <div className="flex h-dvh overflow-hidden">
      <Sidebar className="hidden lg:flex" />
      <div className="flex flex-1 flex-col overflow-hidden">
        <Header />
        <main className="mesh-gradient-bg flex-1 overflow-y-auto p-4 lg:p-8">
          <div className="max-w-4xl mx-auto space-y-8">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-4xl font-bold text-foreground font-sans">Mindful Journal</h2>
                <p className="mt-1 text-sm text-muted-foreground font-medium">Reflect on your day to unlock AI sentiment insights</p>
              </div>
              <Button variant="outline" className="gap-2 rounded-xl bg-card border-border/50 shadow-sm">
                <History className="size-4" /> View History
              </Button>
            </div>

            <Card className="ambient-shadow border-none overflow-hidden bg-card">
              <CardContent className="p-0">
                <div className="bg-violet-50/50 p-4 border-b border-violet-100 flex items-center gap-3 text-violet-700 text-sm font-medium">
                  <Sparkles className="size-5 text-violet-500" />
                  Our Machine Learning model will privately analyse this entry for burnout patterns once saved.
                </div>
                <div className="p-6 space-y-4">
                  <textarea 
                    placeholder="How was your day? What's on your mind?..." 
                    className="w-full min-h-[300px] text-lg bg-transparent border-none focus:outline-none resize-none p-2 placeholder:text-muted-foreground text-foreground"
                    value={entry}
                    onChange={(e) => setEntry(e.target.value)}
                  />
                  <div className="flex items-center justify-between pt-4 border-t border-border/50">
                    <div>
                      {isSaved && <span className="text-sm font-medium text-emerald-600">✓ Entry encrypted and saved securely.</span>}
                    </div>
                    <Button 
                      onClick={handleSave}
                      disabled={entry.length === 0}
                      className="rounded-xl gap-2 px-8 py-6 text-base bg-violet-600 text-white hover:bg-violet-700 shadow-md"
                    >
                      <Save className="size-5" /> Save Entry
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>
    </div>
  )
}