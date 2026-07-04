"use client";

import { useState } from "react";
import { ArrowRight, Loader2 } from "lucide-react";
import Sidebar from "@/components/Sidebar";
import ResearchCard from "@/components/ResearchCard";
import { ApiKeys, ChatMessage, DiscordConfig } from "@/lib/types";
import { runResearch } from "@/lib/api";

const EXAMPLES = ["stripe.com", "Tesla", "Microsoft", "OpenAI"];

const STAGES = [
  "Resolving official website…",
  "Crawling site pages…",
  "Gathering public search data…",
  "Running AI analysis…",
  "Identifying competitors…",
  "Building PDF report…",
];

export default function Home() {
  const [keys, setKeys] = useState<ApiKeys>({
    openrouter_api_key: "",
    serper_api_key: "",
    ai_model: "openai/gpt-4o-mini",
  });
  const [discord, setDiscord] = useState<DiscordConfig>({
    bot_token: "",
    channel_id: "",
    applicant_name: "",
    applicant_email: "",
  });
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [stageIdx, setStageIdx] = useState(0);

  const configured = keys.openrouter_api_key && keys.serper_api_key;

  async function handleSubmit(query?: string) {
    const q = (query ?? input).trim();
    if (!q || loading) return;
    if (!configured) {
      setMessages((m) => [...m, { role: "error", content: "Add your OpenRouter and Serper.dev API keys in the sidebar first." }]);
      return;
    }

    setMessages((m) => [...m, { role: "user", content: q }]);
    setInput("");
    setLoading(true);
    setStageIdx(0);

    const stageTimer = setInterval(() => {
      setStageIdx((i) => Math.min(i + 1, STAGES.length - 1));
    }, 1400);

    try {
      const result = await runResearch(q, keys, discord);
      setMessages((m) => [...m, { role: "result", content: result }]);
    } catch (err: any) {
      setMessages((m) => [...m, { role: "error", content: err.message || "Something went wrong." }]);
    } finally {
      clearInterval(stageTimer);
      setLoading(false);
    }
  }

  function handleNewResearch() {
    setMessages([]);
    setInput("");
  }

  return (
    <div className="flex h-screen bg-canvas text-neutral-100">
      <Sidebar keys={keys} setKeys={setKeys} discord={discord} setDiscord={setDiscord} onNewResearch={handleNewResearch} />

      <main className="flex-1 flex flex-col">
        <div className="flex items-center justify-between border-b border-border px-6 py-3 text-sm">
          <span className="font-medium">Company Research</span>
          <span className="flex items-center gap-1.5 text-emerald-400 text-xs">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" /> LIVE
          </span>
        </div>

        <div className="flex-1 overflow-y-auto px-6 py-8 flex flex-col items-center gap-6">
          {messages.length === 0 && (
            <div className="text-center max-w-lg mt-16">
              <div className="text-[10px] tracking-[0.2em] uppercase text-amber-400 font-semibold mb-3">
                AI-Powered Intelligence
              </div>
              <h1 className="text-3xl font-semibold mb-3">Know any company in minutes.</h1>
              <p className="text-neutral-400 text-sm mb-6">
                Enter a company name or website URL to get AI-powered insights, competitor analysis,
                pain points, and a professional PDF report.
              </p>
              <div className="flex justify-center gap-2 flex-wrap">
                {EXAMPLES.map((ex) => (
                  <button
                    key={ex}
                    onClick={() => handleSubmit(ex)}
                    className="text-xs border border-border rounded-full px-3 py-1.5 hover:bg-white/5"
                  >
                    {ex}
                  </button>
                ))}
              </div>
              {!configured && (
                <p className="text-[11px] text-neutral-600 mt-6">
                  Configure API keys in the sidebar to get started →
                </p>
              )}
            </div>
          )}

          {messages.map((msg, i) => {
            if (msg.role === "user") {
              return (
                <div key={i} className="self-end bg-amber-400 text-black text-sm rounded-2xl px-4 py-2 max-w-md">
                  {msg.content}
                </div>
              );
            }
            if (msg.role === "result") {
              return <ResearchCard key={i} result={msg.content} />;
            }
            if (msg.role === "error") {
              return (
                <div key={i} className="self-start bg-red-500/10 border border-red-500/30 text-red-300 text-sm rounded-xl px-4 py-3 max-w-md">
                  {msg.content}
                </div>
              );
            }
            return null;
          })}

          {loading && (
            <div className="self-start flex items-center gap-2 text-sm text-neutral-400 bg-panel border border-border rounded-xl px-4 py-3">
              <Loader2 size={14} className="animate-spin text-amber-400" />
              {STAGES[stageIdx]}
            </div>
          )}
        </div>

        <div className="border-t border-border px-6 py-4">
          <div className="flex items-center gap-2 max-w-2xl mx-auto">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
              placeholder="Enter a company name (e.g. Aurora Labs) or website URL (e.g. https://aurora.dev)…"
              className="flex-1 bg-panel border border-border rounded-full px-4 py-2.5 text-sm placeholder:text-neutral-600 focus:outline-none focus:ring-1 focus:ring-amber-400"
            />
            <button
              onClick={() => handleSubmit()}
              disabled={loading}
              className="flex items-center gap-1.5 bg-amber-400 hover:bg-amber-500 disabled:opacity-50 text-black text-sm font-medium px-4 py-2.5 rounded-full"
            >
              Research <ArrowRight size={14} />
            </button>
          </div>
          <p className="text-center text-[10px] text-neutral-600 mt-2">
            Enter to research · Shift+Enter for new line
          </p>
        </div>
      </main>
    </div>
  );
}
