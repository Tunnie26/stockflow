import { AuthBrand } from "@/components/auth/auth-brand";
import { AuthHero } from "@/components/auth/auth-hero";
import { LoginForm } from "@/components/auth/login-form";

export default function LoginPage() {
  return (
    <main className="min-h-screen bg-[#03050A] text-[#F4F7FF]">
      <div className="flex min-h-screen">
        {/* Hero - 60% */}
        <AuthHero />

        {/* Login - 40% */}
        <section className="relative flex min-h-screen w-full items-center justify-center overflow-hidden bg-[#090E1A] lg:w-[40%]">
          {/* Astral background */}
          <div className="pointer-events-none absolute inset-0">
            <div className="absolute -right-32 -top-32 size-96 rounded-full bg-[#7C5CFF]/10 blur-3xl" />

            <div className="absolute -bottom-40 -left-40 size-96 rounded-full bg-[#22D3EE]/5 blur-3xl" />
          </div>

          <div className="relative w-full max-w-md px-6 py-10 sm:px-10 lg:px-12 xl:px-16">
            <AuthBrand />

            <div className="mt-12">
              <div>
                <h1 className="text-3xl font-semibold tracking-tight text-[#F4F7FF]">
                  Sign In
                </h1>

                <p className="mt-2 text-sm leading-6 text-[#8490A8]">
                  Enter your credentials to continue
                </p>
              </div>

              <LoginForm />
            </div>

            <p className="mt-10 text-center text-xs text-[#606C84]">
              StockFlow · Inventory Management Platform
            </p>
          </div>
        </section>
      </div>
    </main>
  );
}