"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  Boxes,
  ClipboardCheck,
  LayoutDashboard,
  LogIn,
  LogOut,
  Package,
  Settings,
} from "lucide-react";

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { useAuth } from "@/features/auth/auth-context";

import stockflowLogo from "@/assets/images/stockflow_logo_horizontal.png"

const navigationItems = [
  {
    title: "Thống kê",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    title: "Nhập kho",
    href: "/inbound",
    icon: LogIn,
  },
  {
    title: "Xuất kho",
    href: "/outbound",
    icon: Package,
  },
  {
    title: "Tồn kho",
    href: "/inventory",
    icon: Boxes,
  },
  {
    title: "Kiểm kê",
    href: "/inventory-check",
    icon: ClipboardCheck,
  },
];

const footerItems = [
  {
    title: "Cài đặt",
    href: "/settings",
    icon: Settings,
  },
];

const sidebarItemClassName = [
  "cursor-pointer",
  "h-11 rounded-xl px-3",
  "text-(--sf-text-secondary)",
  "transition-all duration-200",

  "hover:bg-(--sf-interaction-hover)",
  "hover:text-(--sf-text-primary)",

  "focus:outline-none",
  "focus-visible:outline-none",
  "focus-visible:ring-1",
  "focus-visible:ring-(--sf-border-primary)",

  "data-[active=true]:bg-(--sf-interaction-active)",
  "data-[active=true]:text-(--sf-text-primary)",
  "data-[active=true]:shadow-[inset_3px_0_0_var(--sf-primary)",
].join(" ")

export function AppSidebar() {
  const router = useRouter();
  const pathname = usePathname();
  const { logout } = useAuth()

  const isActive = (href: string) => {
    return pathname === href || pathname.startsWith(`${href}/`);
  };

  return (
    <Sidebar
      collapsible="icon"
      className="border-r border-(--sf-border-subtle) bg-(--sf-space-900)"
    >
      {/* Header */}
      <SidebarHeader className="border-b border-(--sf-border-subtle) bg-(--sf-space-900) h-20">
        <div className="flex h-20 items-center px-2">
          <Link href="/dashboard" className="flex min-w-0 items-center">
            <Image
              src={stockflowLogo}
              alt="StockFlow"
              width={180}
              height={48}
              priority
              className="h-auto w-60 object-contain"
            />
          </Link>
        </div>
      </SidebarHeader>

      {/* Navigation */}
      <SidebarContent className="bg-(--sf-space-900) px-3 py-4">
        <SidebarMenu className="gap-1">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.href);

            return (
              <SidebarMenuItem key={item.href}>
                <SidebarMenuButton
                  isActive={active}
                  tooltip={item.title}
                  onClick={() => router.push(item.href)}
                  className={sidebarItemClassName}
                >
                  <Icon
                    className={[
                      "size-4.5 shrink-0",
                      active
                        ? "text-(--sf-primary)"
                        : "text-(--sf-text-tertiary)",
                    ].join(" ")}
                  />

                  <span className="text-sm font-medium">{item.title}</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            );
          })}
        </SidebarMenu>
      </SidebarContent>

      {/* Footer */}
      <SidebarFooter className="border-t border-(--sf-border-subtle) bg-(--sf-space-900) px-3 py-3">
        <SidebarMenu className="gap-1">
          {footerItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.href);

            return (
              <SidebarMenuItem key={item.href}>
                <SidebarMenuButton
                  isActive={active}
                  tooltip={item.title}
                  onClick={() => router.push(item.href)}
                  className={sidebarItemClassName}
                >
                  <Icon
                    className={[
                      "size-4.5 shrink-0",
                      active
                        ? "text-(--sf-primary)"
                        : "text-(--sf-text-tertiary)",
                    ].join(" ")}
                  />

                  <span className="text-sm font-medium">{item.title}</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            );
          })}

          {/* Logout */}
          <SidebarMenuItem>
            <SidebarMenuButton
              tooltip="Logout"
              className={[
                "cursor-pointer",
                "h-11 rounded-xl px-3",
                "text-(--sf-text-secondary)",
                "transition-all duration-200",

                // Hover
                "hover:bg-[color-mix(in_srgb,var(--sf-danger)_8%,transparent)]",
                "hover:text-(--sf-danger)",

                // Keyboard focus
                "focus:outline-none",
                "focus-visible:outline-none",
                "focus-visible:ring-1",
                "focus-visible:ring-(--sf-danger)",
              ].join(" ")}
              onClick={logout}
            >
              <LogOut className="size-4.5 shrink-0 text-(--sf-text-tertiary)" />

              <span className="text-sm font-medium">Đăng xuất</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
}