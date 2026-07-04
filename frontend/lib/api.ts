import { ApiKeys, DiscordConfig, ResearchResponse } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function runResearch(
  query: string,
  keys: ApiKeys,
  discord?: DiscordConfig
): Promise<ResearchResponse> {
  const res = await fetch(`${API_BASE}/api/research`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query,
      keys,
      discord: discord?.bot_token
        ? {
            bot_token: discord.bot_token,
            channel_id: discord.channel_id,
            applicant_name: discord.applicant_name,
            applicant_email: discord.applicant_email,
          }
        : null,
    }),
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(body.detail || "Research request failed.");
  }

  return res.json();
}

export function downloadPdf(base64: string, companyName: string) {
  const byteChars = atob(base64);
  const byteNumbers = new Array(byteChars.length);
  for (let i = 0; i < byteChars.length; i++) {
    byteNumbers[i] = byteChars.charCodeAt(i);
  }
  const byteArray = new Uint8Array(byteNumbers);
  const blob = new Blob([byteArray], { type: "application/pdf" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${companyName.replace(/\s+/g, "_").toLowerCase()}-research-report.pdf`;
  a.click();
  URL.revokeObjectURL(url);
}
