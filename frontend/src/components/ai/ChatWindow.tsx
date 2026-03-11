// frontend/src/components/ai/ChatWindow.tsx
"use client";

import { useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";
import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

interface ChatWindowProps {
  messages: Message[];
  isLoading: boolean;
}

export default function ChatWindow({ messages, isLoading }: ChatWindowProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-6">
      {/* Welcome Message if no messages */}
      {messages.length === 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="flex flex-col items-center justify-center h-full text-center py-16"
        >
          <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-purple-500 rounded-2xl flex items-center justify-center mb-6">
            <Sparkles className="w-8 h-8 text-white" />
          </div>
          <h3 className="text-xl font-semibold text-white mb-2">
            AI Financial Advisor
          </h3>
          <p className="text-gray-400 max-w-md mb-8">
            Ask me anything about your startup&apos;s financial health. I can
            analyze your CAC, LTV, burn rate, runway, and provide actionable
            recommendations.
          </p>

          {/* Example Questions */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-lg w-full">
            {[
              "Is my CAC too high?",
              "How can I improve my LTV?",
              "Is my burn rate sustainable?",
              "How much runway do I have?",
            ].map((question) => (
              <div
                key={question}
                className="px-4 py-3 bg-white/5 border border-dashboard-border rounded-xl text-sm text-gray-400 text-left"
              >
                &ldquo;{question}&rdquo;
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Messages */}
      {messages.map((message) => (
        <ChatMessage
          key={message.id}
          role={message.role}
          content={message.content}
          timestamp={message.timestamp}
        />
      ))}

      {/* Loading indicator */}
      {isLoading && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex gap-3"
        >
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center flex-shrink-0">
            <Sparkles className="w-4 h-4 text-white" />
          </div>
          <div className="bg-dashboard-card border border-dashboard-border rounded-2xl rounded-bl-sm px-4 py-3">
            <div className="flex items-center gap-2">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
              </div>
              <span className="text-xs text-gray-500 ml-2">AI is thinking...</span>
            </div>
          </div>
        </motion.div>
      )}

      {/* Scroll anchor */}
      <div ref={bottomRef} />
    </div>
  );
}