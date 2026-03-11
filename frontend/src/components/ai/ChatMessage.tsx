// frontend/src/components/ai/ChatMessage.tsx
"use client";

import { motion } from "framer-motion";
import { User, Sparkles } from "lucide-react";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
  timestamp?: string;
}

export default function ChatMessage({ role, content, timestamp }: ChatMessageProps) {
  const isUser = role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex gap-3 ${isUser ? "flex-row-reverse" : "flex-row"}`}
    >
      {/* Avatar */}
      <div
        className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
          isUser
            ? "bg-primary-600"
            : "bg-gradient-to-br from-purple-500 to-pink-500"
        }`}
      >
        {isUser ? (
          <User className="w-4 h-4 text-white" />
        ) : (
          <Sparkles className="w-4 h-4 text-white" />
        )}
      </div>

      {/* Message Bubble */}
      <div
        className={`max-w-[75%] rounded-2xl px-4 py-3 ${
          isUser
            ? "bg-primary-600 text-white rounded-br-sm"
            : "bg-dashboard-card border border-dashboard-border text-gray-200 rounded-bl-sm"
        }`}
      >
        {/* Message Content */}
        <div className="text-sm leading-relaxed whitespace-pre-wrap">
          {content}
        </div>

        {/* Timestamp */}
        {timestamp && (
          <p
            className={`text-xs mt-2 ${
              isUser ? "text-primary-200" : "text-gray-500"
            }`}
          >
            {formatTime(timestamp)}
          </p>
        )}
      </div>
    </motion.div>
  );
}

function formatTime(timestamp: string): string {
  try {
    const date = new Date(timestamp);
    return date.toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return "";
  }
}