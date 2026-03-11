// frontend/src/hooks/useChat.ts
"use client";

import { useState, useCallback } from "react";
import api from "@/lib/api";
import { ChatMessage } from "@/types/chat";

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadHistory = useCallback(async () => {
    try {
      const response = await api.get("/api/v1/ai/chat/history");
      const history = response.data.messages.map((msg: any) => ({
        id: String(msg.id),
        role: msg.role,
        content: msg.content,
        timestamp: msg.created_at,
      }));
      setMessages(history);
    } catch (err) {
      console.error("Failed to load chat history:", err);
    }
  }, []);

  const sendMessage = useCallback(async (content: string) => {
    // Add user message immediately
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: "user",
      content,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await api.post("/api/v1/ai/chat", {
        message: content,
      });

      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.data.content,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to send message");
      // Remove the user message if sending failed
      setMessages((prev) => prev.filter((m) => m.id !== userMessage.id));
    } finally {
      setIsLoading(false);
    }
  }, []);

  const clearHistory = useCallback(async () => {
    try {
      await api.delete("/api/v1/ai/chat/history");
      setMessages([]);
    } catch (err) {
      console.error("Failed to clear history:", err);
    }
  }, []);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    loadHistory,
    clearHistory,
  };
}