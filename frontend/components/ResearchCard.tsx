"use client";

import { Download, CheckCircle2 } from "lucide-react";
import { ResearchResponse } from "@/lib/types";
import { downloadPdf } from "@/lib/api";

export default function ResearchCard({ result }: { result: ResearchResponse }) {
  const { company, competitors, pdf_base64, sent_to_discord } = result;

  return (
    <div className="bg-panel border border-border rounded-xl p-6 max-w-2xl w-full">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h2 className="text-lg font-semibold">{company.name}</h2>
          {company.website && (
            <a href={company.website} target="_blank" rel="noreferrer" className="text-xs text-amber-400 hover:underline">
              {company.website}
            </a>
          )}
        </div>
        <span className="text-[10px] uppercase tracking-wide bg-emerald-500/15 text-emerald-400 px-2 py-1 rounded-full">
          Research Complete
        </span>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-5 text-sm">
        <InfoBlock label="Phone" value={company.phone || "Not publicly listed"} />
        <InfoBlock label="Address" value={company.address || "Not publicly listed"} />
      </div>

      <Section title="Products & Services">
        <div className="flex flex-wrap gap-2">
          {company.products_services.map((p, i) => (
            <span key={i} className="text-xs bg-white/5 border border-border rounded-full px-3 py-1">
              {p}
            </span>
          ))}
        </div>
      </Section>

      <Section title="AI-Generated Pain Points">
        <ul className="space-y-1.5 text-sm text-neutral-300 list-disc list-inside">
          {company.pain_points.map((p, i) => (<li key={i}>{p}</li>))}
        </ul>
      </Section>

      <Section title="Competitors">
        <div className="grid grid-cols-2 gap-3">
          {competitors.length === 0 && (
            <span className="text-sm text-neutral-500">No competitors identified.</span>
          )}
          {competitors.map((c, i) => (
            <div key={i} className="border border-border rounded-md p-2">
              <div className="text-sm font-medium">{c.name}</div>
              {c.website && (
                <a href={c.website} target="_blank" rel="noreferrer" className="text-xs text-amber-400 hover:underline break-all">
                  {c.website}
                </a>
              )}
            </div>
          ))}
        </div>
      </Section>

      <div className="flex items-center gap-3 mt-5">
        <button
          onClick={() => downloadPdf(pdf_base64, company.name)}
          className="flex items-center gap-2 bg-amber-400 hover:bg-amber-500 text-black text-sm font-medium px-4 py-2 rounded-md"
        >
          <Download size={14} /> Download PDF Report
        </button>
        {sent_to_discord && (
          <span className="flex items-center gap-1 text-xs text-emerald-400 bg-emerald-500/10 px-3 py-2 rounded-md">
            <CheckCircle2 size={14} /> Sent to Discord
          </span>
        )}
      </div>
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="mb-5">
      <div className="text-[10px] uppercase tracking-wide text-amber-400 font-semibold mb-2">{title}</div>
      {children}
    </div>
  );
}

function InfoBlock({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="text-[10px] uppercase tracking-wide text-neutral-500">{label}</div>
      <div className="text-neutral-200">{value}</div>
    </div>
  );
}
