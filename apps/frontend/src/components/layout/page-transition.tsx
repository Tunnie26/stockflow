"use client";

import {
  createContext,
  useCallback,
  useContext,
  useState,
  type ReactNode,
} from "react";

interface PageTransitionContextValue {
  startTransition: (callback: () => void) => void;
}

const PageTransitionContext = createContext<PageTransitionContextValue | null>(
  null,
);

export function PageTransitionProvider({ children }: { children: ReactNode }) {
  const [isLeaving, setIsLeaving] = useState(false);

  const startTransition = useCallback((callback: () => void) => {
    setIsLeaving(true);

    window.setTimeout(() => {
      callback();
    }, 180);
  }, []);

  return (
    <PageTransitionContext.Provider value={{ startTransition }}>
      <div
        className={[
          "min-h-full transition-opacity duration-180 ease-out",
          isLeaving ? "opacity-0" : "opacity-100",
        ].join(" ")}
      >
        {children}
      </div>
    </PageTransitionContext.Provider>
  );
}

export function usePageTransition() {
  const context = useContext(PageTransitionContext);

  if (!context) {
    throw new Error(
      "usePageTransition must be used within PageTransitionProvider.",
    );
  }

  return context;
}
