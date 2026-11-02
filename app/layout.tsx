import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "Kingdom AI OS", description: "Obi AI — Hermes agent swarm with a deep-research model ensemble." };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (<html lang="en"><body>{children}</body></html>);
}
