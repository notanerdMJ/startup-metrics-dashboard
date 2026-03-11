// frontend/src/types/chat.ts

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface AIInsight {
  id: number;
  insight_type: string;
  insight_text: string;
  severity: 'good' | 'warning' | 'critical';
  recommendation: string;
}