"use client"

import { useState } from "react"
import { MoreHorizontal, Plus, Search, UserCog, Trash2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"

//mock data will swap this with API fetch later
const initialUsers =[
  { id: 1, name: "Melisa Sistek", email: "melisa@stmarys.com", role: "Employee", department: "Testing", status: "Active" },
  { id: 2, name: "Sofia Lavrekhina", email: "sofia@stmarys.com", role: "Admin", department: "Engineering", status: "Active" },
  { id: 3, name: "Gadah Bengalha", email: "gadah@stmarys.com", role: "Manager", department: "IT", status: "Active" },
  { id: 4, name: "Mohamed Anas", email: "anas@stmarys.com", role: "Employee", department: "Engineering", status: "Active" },
]

export function UsersTable() {
  const [users, setUsers] = useState(initialUsers)

  return (
    <Card className="border-border/50 shadow-sm">
      <CardHeader className="flex flex-row items-center justify-between pb-4 border-b border-border/50">
        <CardTitle className="text-xl font-bold">Directory</CardTitle>
        <div className="flex items-center gap-3">
          <div className="relative w-64 hidden sm:block">
            <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
            <Input placeholder="Search users..." className="pl-9 bg-muted/50 border-none rounded-xl" />
          </div>
          <Button className="rounded-xl gap-2">
            <Plus className="size-4" /> Add User
          </Button>
        </div>
      </CardHeader>
      <CardContent className="p-0">
        <Table>
          <TableHeader className="bg-muted/30">
            <TableRow>
              <TableHead className="w-[100px]">ID</TableHead>
              <TableHead>User Details</TableHead>
              <TableHead>Role</TableHead>
              <TableHead>Department</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {users.map((user) => (
              <TableRow key={user.id}>
                <TableCell className="font-medium text-muted-foreground">#{user.id}</TableCell>
                <TableCell>
                  <p className="font-semibold text-foreground">{user.name}</p>
                  <p className="text-xs text-muted-foreground">{user.email}</p>
                </TableCell>
                <TableCell>
                  <Badge variant="outline" className="bg-slate-50 text-slate-700">
                    {user.role}
                  </Badge>
                </TableCell>
                <TableCell>{user.department}</TableCell>
                <TableCell>
                  <Badge className={user.status === "Active" ? "bg-emerald-100 text-emerald-700 hover:bg-emerald-100" : "bg-gray-100 text-gray-700 hover:bg-gray-100"}>
                    {user.status}
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
                      <DropdownMenuItem className="gap-2 cursor-pointer"><UserCog className="size-4" /> Edit Role</DropdownMenuItem>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem className="gap-2 text-destructive cursor-pointer focus:text-destructive"><Trash2 className="size-4" /> Deactivate</DropdownMenuItem>
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