import Image from "next/image";

import loginTheme from "@/assets/images/stockflow_login_theme.png";

export function AuthHero() {
  return (
    <section
      aria-label="StockFlow inventory management"
      className="relative hidden h-full min-h-screen overflow-hidden lg:block lg:w-[60%]"
    >
      <Image
        src={loginTheme}
        alt="StockFlow inventory management"
        fill
        priority
        sizes="60vw"
        className="object-cover object-center"
      />

      <div className="absolute inset-0 bg-gradient-to-r from-[#03050A]/20 via-transparent to-[#03050A]/30" />

      <div className="absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-[#03050A]/30 to-transparent" />
    </section>
  );
}