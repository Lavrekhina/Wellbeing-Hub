import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"
import { BrainCircuit, ShieldCheck, UserCircle, Zap } from "lucide-react"

export function HelpContent() {
  return (
    <div className="space-y-6">
      {/* AI Transparency Section */}
      <section className="space-y-4">
        <div className="flex items-center gap-2 mb-2">
          <BrainCircuit className="size-5 text-primary" />
          <h3 className="text-xl font-bold text-foreground">How our AI works</h3>
        </div>
        
        <Accordion type="single" collapsible className="w-full space-y-3">
          <AccordionItem value="item-1" className="bg-card px-6 rounded-2xl border border-border/50 ambient-shadow">
            <AccordionTrigger className="hover:no-underline font-semibold py-5">
              What is the "Weighted Risk Algorithm"?
            </AccordionTrigger>
            <AccordionContent className="text-muted-foreground leading-relaxed pb-5">
              Unlike traditional surveys that simply average your scores, our AI uses a <strong>Weighted Algorithmic Model</strong>. 
              This means the system looks for intensity patterns—for example, if you report high stress levels consistently over 48 hours, 
              the system "weighs" that more heavily than a single bad morning, allowing for earlier burnout identification.
            </AccordionContent>
          </AccordionItem>

          <AccordionItem value="item-2" className="bg-card px-6 rounded-2xl border border-border/50 ambient-shadow">
            <AccordionTrigger className="hover:no-underline font-semibold py-5">
              How are my personalised recommendations generated?
            </AccordionTrigger>
            <AccordionContent className="text-muted-foreground leading-relaxed pb-5">
              Recommendations are mapped dynamically based on your calculated risk level. The system cross-references your 
              check-in categories (e.g. sleep, workload, mood) with a library of evidence-based support resources to provide 
              the most relevant guidance for your current state.
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      </section>

      {/* Privacy Section */}
      <section className="space-y-4">
        <div className="flex items-center gap-2 mb-2">
          <ShieldCheck className="size-5 text-emerald-600" />
          <h3 className="text-xl font-bold text-foreground">Privacy & Data Handling</h3>
        </div>

        <Accordion type="single" collapsible className="w-full space-y-3">
          <AccordionItem value="privacy-1" className="bg-card px-6 rounded-2xl border border-border/50 ambient-shadow">
            <AccordionTrigger className="hover:no-underline font-semibold py-5">
              Can my manager see my individual results?
            </AccordionTrigger>
            <AccordionContent className="text-muted-foreground leading-relaxed pb-5">
              <strong>Absolutely not.</strong> Our platform is built on <strong>K-Anonymisation</strong> standards. 
              Management dashboards only show aggregated trends. If a department has fewer than 3 respondents, the data 
              is automatically hidden to ensure no individual can be identified.
            </AccordionContent>
          </AccordionItem>

          <AccordionItem value="privacy-2" className="bg-card px-6 rounded-2xl border border-border/50 ambient-shadow">
            <AccordionTrigger className="hover:no-underline font-semibold py-5">
              How do I withdraw my consent?
            </AccordionTrigger>
            <AccordionContent className="text-muted-foreground leading-relaxed pb-5">
              You have the "Right to be Forgotten" under GDPR. You can withdraw your consent at any time via the 
              Settings page, which will immediately cease data processing and hide your historical records from 
              organisational aggregates.
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      </section>
    </div>
  )
}