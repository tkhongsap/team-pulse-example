"use client";

import { useRef, useEffect, useState } from "react";
import { MarkdownRenderer } from "./markdown-renderer";
import { SourceCitations } from "./source-citations";
import { SuggestedQuestions } from "./suggested-questions";
import { getAnonymousId } from "@/lib/anonymous-id";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: string[];
}

export function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height =
        Math.min(textareaRef.current.scrollHeight, 200) + "px";
    }
  }, [input]);

  // Restore session from sessionStorage
  useEffect(() => {
    const stored = sessionStorage.getItem("teamPulseSessionId");
    if (stored) setSessionId(stored);
  }, []);

  const sendMessage = async () => {
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: trimmed,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    const assistantId = crypto.randomUUID();

    try {
      const response = await fetch("/api/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Team-Pulse-Id": getAnonymousId(),
        },
        body: JSON.stringify({ question: trimmed, sessionId }),
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({ error: "Request failed" }));
        setMessages((prev) => [
          ...prev,
          {
            id: assistantId,
            role: "assistant",
            content: `Error: ${err.error || "Request failed"}`,
          },
        ]);
        setIsLoading(false);
        return;
      }

      const contentType = response.headers.get("content-type") || "";

      if (contentType.includes("text/event-stream") && response.body) {
        // SSE streaming
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split("\n");
          buffer = lines.pop() || "";

          let currentEvent = "";
          for (const line of lines) {
            if (line.startsWith("event: ")) {
              currentEvent = line.slice(7);
            } else if (line.startsWith("data: ")) {
              const data = line.slice(6);
              try {
                const parsed = JSON.parse(data);
                if (currentEvent === "result" && parsed.text) {
                  const sources: string[] = parsed.sources || [];
                  setMessages((prev) => {
                    const existing = prev.find((m) => m.id === assistantId);
                    if (existing) {
                      return prev.map((m) =>
                        m.id === assistantId
                          ? { ...m, content: parsed.text, sources }
                          : m
                      );
                    }
                    return [
                      ...prev,
                      {
                        id: assistantId,
                        role: "assistant" as const,
                        content: parsed.text,
                        sources,
                      },
                    ];
                  });
                  if (parsed.sessionId) {
                    setSessionId(parsed.sessionId);
                    sessionStorage.setItem(
                      "teamPulseSessionId",
                      parsed.sessionId
                    );
                  }
                }
              } catch {
                // Skip invalid JSON
              }
            }
          }
        }
      } else {
        // JSON response (fallback when server not available)
        const data = await response.json();
        setMessages((prev) => [
          ...prev,
          {
            id: assistantId,
            role: "assistant",
            content: data.error || data.text || "No response",
          },
        ]);
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          id: assistantId,
          role: "assistant",
          content:
            "Could not connect to the ask server. Start it with: `python3 scripts/ask_server.py`",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        {messages.length === 0 && (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <h2 className="text-2xl font-semibold text-foreground">
                Team Pulse
              </h2>
              <p className="mt-2 text-muted-foreground">
                Ask anything about your team
              </p>
              <SuggestedQuestions
                onSelect={(question) => {
                  setInput(question);
                  // Auto-send after a tick to let state update
                  setTimeout(() => {
                    const textarea = textareaRef.current;
                    if (textarea) {
                      textarea.focus();
                    }
                  }, 0);
                }}
              />
            </div>
          </div>
        )}

        <div className="max-w-3xl mx-auto space-y-6">
          {messages.map((message) => (
            <div key={message.id}>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs font-medium text-muted-foreground">
                  {message.role === "user" ? "You" : "Team Pulse"}
                </span>
              </div>
              <div
                className={`rounded-lg px-4 py-3 ${
                  message.role === "user"
                    ? "bg-[#f3f4f6] dark:bg-[#334155]"
                    : "bg-white dark:bg-[#1e293b]"
                }`}
              >
                {message.role === "assistant" ? (
                  <>
                    <MarkdownRenderer content={message.content} />
                    {message.sources && message.sources.length > 0 && (
                      <SourceCitations sources={message.sources} />
                    )}
                  </>
                ) : (
                  <p className="text-sm whitespace-pre-wrap">
                    {message.content}
                  </p>
                )}
              </div>
            </div>
          ))}

          {isLoading && !messages.find((m) => m.role === "assistant" && m.id === messages[messages.length - 1]?.id) && (
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs font-medium text-muted-foreground">
                  Team Pulse
                </span>
              </div>
              <div className="rounded-lg px-4 py-3 bg-white dark:bg-[#1e293b]">
                <div className="flex gap-1">
                  <span className="w-2 h-2 rounded-full bg-muted-foreground/40 animate-bounce" />
                  <span className="w-2 h-2 rounded-full bg-muted-foreground/40 animate-bounce [animation-delay:150ms]" />
                  <span className="w-2 h-2 rounded-full bg-muted-foreground/40 animate-bounce [animation-delay:300ms]" />
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input area */}
      <div className="border-t border-border bg-background px-4 py-3">
        <div className="max-w-3xl mx-auto flex items-end gap-2">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask anything about your team..."
            rows={1}
            className="flex-1 resize-none rounded-lg border border-border bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary"
          />
          <button
            onClick={sendMessage}
            disabled={!input.trim() || isLoading}
            className="shrink-0 h-9 px-4 rounded-lg bg-primary text-primary-foreground text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-primary/90 transition-colors"
          >
            {isLoading ? (
              <svg
                className="w-4 h-4 animate-spin"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                />
              </svg>
            ) : (
              "Send"
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
