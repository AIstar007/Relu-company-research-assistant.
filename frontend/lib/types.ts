export interface CompanyInfo {
  name: string;
  website?: string | null;
  phone?: string | null;
  address?: string | null;
  products_services: string[];
  pain_points: string[];
  summary?: string | null;
}

export interface Competitor {
  name: string;
  website?: string | null;
}

export interface ResearchResponse {
  company: CompanyInfo;
  competitors: Competitor[];
  pdf_base64: string;
  sent_to_discord: boolean;
  sources_crawled: string[];
}

export interface ApiKeys {
  openrouter_api_key: string;
  serper_api_key: string;
  ai_model: string;
}

export interface DiscordConfig {
  bot_token: string;
  channel_id: string;
  applicant_name: string;
  applicant_email: string;
}

export type ChatMessage =
  | { role: "user"; content: string }
  | { role: "progress"; content: string }
  | { role: "result"; content: ResearchResponse }
  | { role: "error"; content: string };
