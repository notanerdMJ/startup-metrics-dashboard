// frontend/src/components/ui/Loading.tsx
"use client";

import { cn } from "@/lib/utils";

interface LoadingProps {
  size?: "sm" | "md" | "lg";
  text?: string;
  className?: string;
}

export default function Loading({ size = "md", text, className }: LoadingProps) {
  const sizes = {
    sm: "h-6 w-6",
    md: "h-10 w-10",
    lg: "h-16 w-16",
  };

  return (
    <div className={cn("flex flex-col items-center justify-center gap-3", className)}>
      <div className={cn("relative", sizes[size])}>
        <div className="absolute inset-0 rounded-full border-2 border-primary-500/20" />
        <div className="absolute inset-0 rounded-full border-2 border-transparent border-t-primary-500 animate-spin" />
      </div>
      {text && (
        <p className="text-sm text-gray-400 animate-pulse">{text}</p>
      )}
    </div>
  );
}