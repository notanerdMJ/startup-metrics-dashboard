// frontend/src/components/ui/Card.tsx
"use client";

import { cn } from "@/lib/utils";
import { HTMLAttributes } from "react";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "glass" | "bordered";
  hover?: boolean;
}

export default function Card({
  className,
  variant = "default",
  hover = true,
  children,
  ...props
}: CardProps) {
  const variants = {
    default: "bg-dashboard-card border border-dashboard-border",
    glass: "bg-white/5 backdrop-blur-xl border border-white/10",
    bordered: "bg-transparent border-2 border-dashboard-border",
  };

  return (
    <div
      className={cn(
        "rounded-xl p-6",
        "transition-all duration-300",
        variants[variant],
        hover && "hover:border-primary-500/30 hover:shadow-lg hover:shadow-primary-500/5",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}