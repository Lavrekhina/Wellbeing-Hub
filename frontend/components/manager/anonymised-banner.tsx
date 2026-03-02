import { ShieldCheck } from "lucide-react"

export function AnonymisedBanner() {
  return (
    <div className="flex items-center gap-3 rounded-2xl border border-emerald-200/60 bg-emerald-50 px-5 py-4">
      <ShieldCheck className="size-5 text-emerald-600 shrink-0" />
      <p className="text-sm font-medium text-emerald-800">
        All data shown is fully anonymised. No individual employee data is visible or accessible from this view.
      </p>
    </div>
  )
}