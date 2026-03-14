// frontend/src/types/metrics.ts

export interface MetricsSummary {
  total_records: number;
  total_ad_spend: number;
  total_conversions: number;
  overall_cac: number;
  average_ltv: number;
  ltv_cac_ratio: number;
  estimated_burn_rate: number;
  estimated_runway_months: number;
  is_healthy: boolean;
}

export interface ChannelMetrics {
  channel: string;
  ad_spend: number;
  conversions: number;
  cac: number;
  conversion_rate: number;
  roi: number;
}

export interface DashboardCard {
  title: string;
  value: string;
  change: number;
  trend: string;
  description: string;
}