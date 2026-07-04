import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Company Research | Relu Consultancy",
  description: "AI-powered company research assistant",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
