"use client";

import "./globals.css";
import { ReactNode } from "react";
import { Navbar } from "@/components/Navbar";
import { WagmiProvider } from "wagmi";
import { wagmiConfig } from "@/wagmiConfig";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gradient-to-tr from-blue-400 via-purple-500 to-pink-500 animate-gradient min-h-screen text-white">
        <WagmiProvider config={wagmiConfig}>
          <QueryClientProvider client={queryClient}>
            <Navbar />
            {children}
          </QueryClientProvider>
        </WagmiProvider>
      </body>
    </html>
  );
}
