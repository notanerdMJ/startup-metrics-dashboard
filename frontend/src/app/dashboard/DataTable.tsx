// frontend/src/components/dashboard/DataTable.tsx
"use client";

import { cn } from "@/lib/utils";
import { motion } from "framer-motion";

interface Column {
  key: string;
  label: string;
  format?: (value: any) => string;
  color?: (value: any) => string;
}

interface DataTableProps {
  title: string;
  columns: Column[];
  data: any[];
  className?: string;
}

export default function DataTable({ title, columns, data, className }: DataTableProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={cn(
        "bg-dashboard-card border border-dashboard-border rounded-xl overflow-hidden",
        className
      )}
    >
      <div className="px-6 py-4 border-b border-dashboard-border">
        <h3 className="text-lg font-semibold text-white">{title}</h3>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-dashboard-border">
              {columns.map((col) => (
                <th
                  key={col.key}
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {col.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, i) => (
              <tr
                key={i}
                className="border-b border-dashboard-border/50 hover:bg-dashboard-hover transition-colors"
              >
                {columns.map((col) => {
                  const value = row[col.key];
                  const formatted = col.format ? col.format(value) : String(value);
                  const colorClass = col.color ? col.color(value) : "text-gray-300";

                  return (
                    <td key={col.key} className={cn("px-6 py-4 text-sm", colorClass)}>
                      {formatted}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </motion.div>
  );
}