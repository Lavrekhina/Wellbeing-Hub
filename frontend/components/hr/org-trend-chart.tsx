"use client"

import { Card, CardContent } from "@/components/ui/card"
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"

const dummyTrendData = [
  { month: "Oct", risk: 24 },
  { month: "Nov", risk: 28 },
  { month: "Dec", risk: 42 },
  { month: "Jan", risk: 35 },
  { month: "Feb", risk: 38 },
  { month: "Mar", risk: 31 },
]

export function OrgTrendChart({ isRealData }: { isRealData: boolean }) {
  return (
    <Card className="py-6">
      <CardContent className="space-y-4">
        <div>
          <h3 className="text-xl font-semibold text-foreground font-sans">Global Wellbeing Trend</h3>
          <p className="text-sm text-muted-foreground">Average organization risk score over the last 6 months</p>
        </div>

        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={dummyTrendData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="orgRiskGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#8b5cf6" stopOpacity={0.2} />
                  <stop offset="100%" stopColor="#8b5cf6" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
              <XAxis 
                dataKey="month" 
                axisLine={false} 
                tickLine={false} 
                tick={{fontSize: 12, fill: '#64748b'}} 
              />
              <YAxis domain={[0, 100]} axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#64748b'}} />
              <Tooltip 
                contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
              />
              <Area
                type="monotone"
                dataKey="risk"
                stroke="#8b5cf6"
                strokeWidth={3}
                fill="url(#orgRiskGradient)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  )
}