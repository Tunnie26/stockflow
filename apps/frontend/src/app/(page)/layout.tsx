import { AppShell } from "@/components/layout/app-shell";
import React from "react";

export default function PageLayout({children}: {children: React.ReactNode}){
    return (
        <AppShell>{children}</AppShell>
    )
}