"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { ShieldAlert, Trash2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"

export function PrivacySettings() {
  const router = useRouter()
  const[isRevoking, setIsRevoking] = useState(false)

  const handleRevokeConsent = async () => {
    setIsRevoking(true)
    // Simulate API delay, then kick them out to the login screen
    setTimeout(() => {
      setIsRevoking(false)
      router.push("/login") 
    }, 1500)
  }

  return (
    <div className="space-y-6">
      <Card className="border-destructive/20 shadow-sm bg-destructive/5">
        <CardHeader className="border-b border-destructive/10 pb-4">
          <div className="flex items-center gap-2 text-destructive">
            <ShieldAlert className="size-5" />
            <CardTitle className="text-xl">Data & Consent Management</CardTitle>
          </div>
          <CardDescription className="text-destructive/80">
            Manage your GDPR rights and platform data access.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6 pt-6">
          
          <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
            <div className="space-y-2 max-w-2xl">
              <h4 className="font-semibold text-foreground">Revoke Platform Consent</h4>
              <p className="text-sm text-muted-foreground leading-relaxed">
                By revoking your consent, you are exercising your "Right to be Forgotten". 
                The Wellbeing Hub will immediately stop processing your data. Your historical 
                journal entries and check-ins will be permanently anonymised or deleted.
              </p>
              <p className="text-sm font-medium text-destructive">
                Note: You will be logged out immediately and will lose access to the dashboard.
              </p>
            </div>

            <AlertDialog>
              <AlertDialogTrigger asChild>
                <Button variant="destructive" className="shrink-0 gap-2 bg-red-600 text-white hover:bg-red-700">
                  <Trash2 className="size-4" />
                  Revoke Consent
                </Button>
              </AlertDialogTrigger>
              
              <AlertDialogContent className="rounded-2xl">
                <AlertDialogHeader>
                  <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                  <AlertDialogDescription>
                    This action cannot be undone. This will permanently revoke your consent to process wellbeing data 
                    and you will be securely logged out of the application.
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel className="rounded-xl">Cancel</AlertDialogCancel>
                  
                  <AlertDialogAction 
                    onClick={handleRevokeConsent}
                    className="rounded-xl bg-red-600 text-white hover:bg-red-700"
                  >
                    {isRevoking ? "Revoking..." : "Yes, revoke my consent"}
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          </div>

        </CardContent>
      </Card>
    </div>
  )
}