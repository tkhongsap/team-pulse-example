import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { AppShell } from "@/components/app-shell";
import { getWikiArticles, getReportDates } from "@/lib/wiki";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Team Pulse",
  description: "Team operations intelligence powered by AI",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const contributors = getWikiArticles("contributors");
  const projects = getWikiArticles("projects");
  const patterns = getWikiArticles("patterns");
  const connections = getWikiArticles("connections");
  const reportDates = getReportDates();

  return (
    <html
      lang="en"
      className={`${inter.variable} ${jetbrainsMono.variable} h-full antialiased`}
    >
      <body className="min-h-full font-sans">
        <AppShell
          contributors={contributors}
          projects={projects}
          patterns={patterns}
          connections={connections}
          reportDates={reportDates}
        >
          {children}
        </AppShell>
      </body>
    </html>
  );
}
