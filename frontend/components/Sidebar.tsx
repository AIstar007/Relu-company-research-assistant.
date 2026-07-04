"use client";

import { useState } from "react";
import { Plus, Check } from "lucide-react";
import { ApiKeys, DiscordConfig } from "@/lib/types";

interface SidebarProps {
  keys: ApiKeys;
  setKeys: (k: ApiKeys) => void;
  discord: DiscordConfig;
  setDiscord: (d: DiscordConfig) => void;
  onNewResearch: () => void;
}

const MODEL_OPTIONS = [
  "openai/gpt-4o-mini",
  "openai/gpt-4o",
  "anthropic/claude-3.5-sonnet",
  "google/gemini-2.0-flash-001",
  "meta-llama/llama-3.1-70b-instruct",
];

export default function Sidebar({ keys, setKeys, discord, setDiscord, onNewResearch }: SidebarProps) {
  const [tab, setTab] = useState<"api" | "discord">("api");
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 1500);
  };

  return (
    <aside className="w-[280px] shrink-0 border-r border-border bg-panel flex flex-col h-full">
      <div className="p-4 border-b border-border">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-6 h-6 rounded bg-amber-400 flex items-center justify-center text-black font-bold text-xs">
            R
          </div>
          <div>
            <div className="text-sm font-semibold leading-none">Relu Consultancy</div>
            <div className="text-[10px] text-neutral-500 tracking-wide uppercase">Company Intelligence</div>
          </div>
        </div>
        <button
          onClick={onNewResearch}
          className="w-full flex items-center justify-center gap-2 text-sm py-2 rounded-md border border-border hover:bg-white/5 transition"
        >
          <Plus size={14} /> New Research
        </button>
      </div>

      <div className="flex border-b border-border text-xs">
        <button
          onClick={() => setTab("api")}
          className={`flex-1 py-2 ${tab === "api" ? "bg-white/5 text-white" : "text-neutral-500"}`}
        >
          API
        </button>
        <button
          onClick={() => setTab("discord")}
          className={`flex-1 py-2 ${tab === "discord" ? "bg-white/5 text-white" : "text-neutral-500"}`}
        >
          DISCORD
        </button>
      </div>

      <div className="p-4 flex-1 overflow-y-auto space-y-4 text-sm">
        {tab === "api" ? (
          <>
            <Field
              label="OpenRouter API Key"
              placeholder="sk-or-v1-..."
              value={keys.openrouter_api_key}
              onChange={(v) => setKeys({ ...keys, openrouter_api_key: v })}
              type="password"
            />
            <Field
              label="Serper.dev API Key"
              placeholder="Your Serper key..."
              value={keys.serper_api_key}
              onChange={(v) => setKeys({ ...keys, serper_api_key: v })}
              type="password"
            />
            <div>
              <label className="block text-[10px] uppercase tracking-wide text-neutral-500 mb-1">
                AI Model
              </label>
              <select
                value={keys.ai_model}
                onChange={(e) => setKeys({ ...keys, ai_model: e.target.value })}
                className="w-full bg-canvas border border-border rounded-md px-2 py-2 text-sm"
              >
                {MODEL_OPTIONS.map((m) => (
                  <option key={m} value={m}>{m}</option>
                ))}
              </select>
            </div>
            <SaveButton onClick={handleSave} saved={saved} />
            <div className="pt-4 border-t border-border text-[11px] text-neutral-500 space-y-2">
              <div className="text-neutral-400 font-medium">How it works</div>
              <ol className="space-y-1 list-decimal list-inside">
                <li>Enter a company name or URL</li>
                <li>Serper.dev searches and crawls it</li>
                <li>OpenRouter AI generates insights</li>
                <li>Download a professional PDF report</li>
              </ol>
            </div>
          </>
        ) : (
          <>
            <div className="bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs rounded-md p-2">
              After research completes, the report auto-sends to your configured channel.
            </div>
            <Field
              label="Bot Token"
              placeholder="Bot token..."
              value={discord.bot_token}
              onChange={(v) => setDiscord({ ...discord, bot_token: v })}
              type="password"
            />
            <Field
              label="Channel ID"
              placeholder="000000000000000000"
              value={discord.channel_id}
              onChange={(v) => setDiscord({ ...discord, channel_id: v })}
            />
            <div className="pt-2 border-t border-border">
              <div className="text-[10px] uppercase tracking-wide text-neutral-500 mb-2">Applicant Details</div>
              <Field
                label="Full Name"
                placeholder="Your full name"
                value={discord.applicant_name}
                onChange={(v) => setDiscord({ ...discord, applicant_name: v })}
              />
              <div className="h-2" />
              <Field
                label="Email Address"
                placeholder="email@example.com"
                value={discord.applicant_email}
                onChange={(v) => setDiscord({ ...discord, applicant_email: v })}
              />
            </div>
            <SaveButton onClick={handleSave} saved={saved} label="Save Discord Config" />
          </>
        )}
      </div>
    </aside>
  );
}

function Field({
  label, placeholder, value, onChange, type = "text",
}: { label: string; placeholder: string; value: string; onChange: (v: string) => void; type?: string }) {
  return (
    <div>
      <label className="block text-[10px] uppercase tracking-wide text-neutral-500 mb-1">{label}</label>
      <input
        type={type}
        value={value}
        placeholder={placeholder}
        onChange={(e) => onChange(e.target.value)}
        className="w-full bg-canvas border border-border rounded-md px-2 py-2 text-sm placeholder:text-neutral-600 focus:outline-none focus:ring-1 focus:ring-amber-400"
      />
    </div>
  );
}

function SaveButton({ onClick, saved, label = "Save Configuration" }: { onClick: () => void; saved: boolean; label?: string }) {
  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center justify-center gap-2 py-2 rounded-md text-sm font-medium transition ${
        saved ? "bg-emerald-600 text-white" : "bg-amber-400 text-black hover:bg-amber-500"
      }`}
    >
      {saved ? (<><Check size={14} /> Saved</>) : label}
    </button>
  );
}
