"use client";

import Image from "next/image";

import logo from "@/assets/images/stockflow_logo_horizontal.png";

export function AuthBrand() {
  return (
    <div className="flex items-center">
      <Image
        src={logo}
        alt="StockFlow"
        priority
        className="h-auto w-[220px] object-contain"
      />
    </div>
  );
}