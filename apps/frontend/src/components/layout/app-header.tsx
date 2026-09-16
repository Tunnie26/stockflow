"use client";

import { Bell, Search } from "lucide-react";
import { useEffect, useRef, useState } from "react";

import { SidebarTrigger } from "@/components/ui/sidebar";
import { useAuth } from "@/features/auth/auth-context";
import { getRoleLabel, getUserInitials } from "@/utils/auth-utils";

import { LanguageSelector } from "./language-selector";
import { WarehouseSelector } from "./warehouse-selector";

export function AppHeader() {
  const searchRef = useRef<HTMLInputElement>(null);
  const [search, setSearch] = useState("");

  const { user } = useAuth();

  const initials = user ? getUserInitials(user.username) : "";
  const roleLabel = user ? getRoleLabel(user.role) : "";

  useEffect(() => {
    const handleShortcut = (event: KeyboardEvent) => {
      if (
        (event.ctrlKey || event.metaKey) &&
        event.key.toLowerCase() === "k"
      ) {
        event.preventDefault();
        searchRef.current?.focus();
        searchRef.current?.select();
      }
    };

    window.addEventListener("keydown", handleShortcut);

    return () => {
      window.removeEventListener("keydown", handleShortcut);
    };
  }, []);

  return (
    <header className="flex h-20 shrink-0 items-center border-b border-[#172136] bg-[#090E1A] px-3 sm:px-4">
      {/* Left */}
      <div className="flex min-w-0 flex-1 items-center gap-2 sm:gap-3">
        <SidebarTrigger className="size-10 shrink-0 cursor-pointer text-[#B8C2D9] hover:bg-[rgba(79,124,255,0.08)] hover:text-[#F4F7FF]" />

        {/* Search desktop / tablet */}
        <div className="relative hidden min-w-0 flex-1 md:block md:max-w-xl lg:max-w-2xl">
          <Search
            className="pointer-events-none absolute left-3.5 top-1/2 size-4.5 -translate-y-1/2 text-[#8490A8]"
            aria-hidden="true"
          />

          <input
            ref={searchRef}
            type="text"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Tìm kiếm toàn cục"
            className="h-11 w-full rounded-lg border border-[#202C43] bg-[#0D1422] pl-10 pr-2 text-sm text-[#F4F7FF] outline-none transition-colors placeholder:text-[#606C84] focus:border-[#5B82FF] focus:ring-2 focus:ring-[#5B82FF]/20"
            aria-label="Tìm kiếm"
          />
        </div>

        {/* Search mobile */}
        <button
          type="button"
          aria-label="Tìm kiếm"
          onClick={() => {
            searchRef.current?.focus();
          }}
          className="flex size-10 cursor-pointer items-center justify-center rounded-lg text-[#B8C2D9] transition-colors hover:bg-[rgba(79,124,255,0.08)] hover:text-[#F4F7FF] md:hidden"
        >
          <Search className="size-5" aria-hidden="true" />
        </button>
      </div>

      {/* Right */}
      <div className="ml-2 flex shrink-0 items-center gap-0.5 sm:ml-4 sm:gap-1">
        {/* Notifications */}
        <button
          type="button"
          aria-label="Thông báo"
          className="relative flex size-10 cursor-pointer items-center justify-center rounded-lg text-[#B8C2D9] transition-colors hover:bg-[rgba(79,124,255,0.08)] hover:text-[#F4F7FF]"
        >
          <Bell className="size-5" aria-hidden="true" />
        </button>

        {/* Warehouse */}
        <div className="ml-0.5 sm:ml-1">
          <WarehouseSelector />
        </div>

        {/* Language */}
        <div className="ml-0.5 sm:ml-1">
          <LanguageSelector />
        </div>

        {/* User */}
        <button
          type="button"
          aria-label="Tài khoản"
          className="ml-0.5 flex h-11 cursor-pointer items-center gap-2 rounded-lg px-1.5 text-left transition-colors hover:bg-[rgba(79,124,255,0.08)] sm:ml-1 sm:px-2.5"
        >
          <span className="flex size-9 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-[#4F7CFF] to-[#7C5CFF] text-xs font-semibold text-white">
            {initials}
          </span>

          <span className="hidden xl:block">
            <span className="block text-sm font-medium text-[#F4F7FF]">
              {user?.username ?? "User"}
            </span>

            <span className="block text-[11px] text-[#8490A8]">
              {roleLabel}
            </span>
          </span>
        </button>
      </div>
    </header>
  );
}