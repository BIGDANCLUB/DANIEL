import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Tech Field Investment Tracker",
  description: "Track VC investment trends across emerging technology fields",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body className="min-h-screen bg-gray-950 text-gray-100 antialiased">
        {children}
      </body>
    </html>
  );
}
