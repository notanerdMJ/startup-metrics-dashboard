// frontend/src/components/charts/ChartWrapper.tsx
"use client";

import dynamic from "next/dynamic";
import { ReactNode } from "react";

// This wrapper ensures charts only render on the client side
export default function ChartWrapper({ children }: { children: ReactNode }) {
  return <>{children}</>;
}