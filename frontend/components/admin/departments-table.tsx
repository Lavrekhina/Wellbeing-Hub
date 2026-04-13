"use client"

import { useState } from "react"
import { MoreHorizontal, Plus, Building2, Trash2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"

// Mock Data
const initialDepartments =[
  { id: 1, name: "Engineering", head: "Alex Turner", count: 24, status: "Active" },
  { id: 2, name: "Sales & Marketing", head: "Sarah Jenkins", count: 18, status: "Active" },
  { id: 3, name: "Customer Support", head: "David Chen", count: 15, status: "Active" },
  { id: 4, name: "Legal", head: "Unassigned", count: 2, status: "Review Required" },
]

export function DepartmentsTable() {
  const [departments, setDepartments] = useState(initialDepartments)

  return (
    <Card className="border-border/50 shadow-sm">
      <CardHeader className="flex flex-row items-center justify-between pb-4 border-b border-border/50">
        <CardTitle className="text-xl font-bold">Organizational Structure</CardTitle>
        <Button className="rounded-xl gap-2 bg-slate-800 hover:bg-slate-700 text-white">
          <Plus className="size-4" /> Add Department
        </Button>
      </CardHeader>
      <CardContent className="p-0">
        <Table>
          <TableHeader className="bg-muted/30">
            <TableRow>
              <TableHead className="w-[100px]">ID</TableHead>
              <TableHead>Department Name</TableHead>
              <TableHead>Department Head</TableHead>
              <TableHead>Employee Count</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {departments.map((dept) => (
              <TableRow key={dept.id}>
                <TableCell className="font-medium text-muted-foreground">#{dept.id}</TableCell>
                <TableCell className="font-semibold text-foreground">{dept.name}</TableCell>
                <TableCell>{dept.head}</TableCell>
                <TableCell>{dept.count} members</TableCell>
                <TableCell>
                  <Badge className={dept.status === "Active" ? "bg-emerald-100 text-emerald-700 hover:bg-emerald-100" : "bg-amber-100 text-amber-700 hover:bg-amber-100"}>
                    {dept.status}
                  </Badge>
                </TableCell>
                <TableCell className="text-right">
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" className="size-8 p-0 rounded-lg">
                        <MoreHorizontal className="size-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end" className="rounded-xl">
                      <DropdownMenuLabel>Actions</DropdownMenuLabel>
                      <DropdownMenuItem className="gap-2 cursor-pointer"><Building2 className="size-4" /> Edit Details</DropdownMenuItem>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem className="gap-2 text-destructive cursor-pointer focus:text-destructive"><Trash2 className="size-4" /> Delete</DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}