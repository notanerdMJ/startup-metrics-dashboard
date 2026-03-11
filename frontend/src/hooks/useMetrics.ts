// frontend/src/hooks/useMetrics.ts
"use client";

import { useState, useEffect } from "react";
import api from "@/lib/api";

export function useMetrics(endpoint: string) {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
  }, [endpoint]);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get(endpoint);
      setData(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to fetch data");
      console.error(`Error fetching ${endpoint}:`, err);
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, refetch: fetchData };
}