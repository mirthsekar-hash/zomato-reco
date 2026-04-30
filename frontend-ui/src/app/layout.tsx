import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Search, Menu, UtensilsCrossed } from "lucide-react";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Reco Partner - Discover Your Taste",
  description: "AI-Powered Restaurant Discovery and Recommendation",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} min-h-screen flex flex-col antialiased bg-[#FAFAFA]`}>
        <header className="bg-white/80 backdrop-blur-md border-b border-gray-100 sticky top-0 z-50">
          <div className="container mx-auto px-6 h-20 flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center gap-2 text-reco-red font-black text-2xl italic tracking-tight group cursor-pointer">
              <UtensilsCrossed size={28} className="group-hover:rotate-12 transition-transform" />
              <span>Reco Partner</span>
            </div>

            {/* Nav */}
            <nav className="hidden md:flex items-center gap-8">
              {["Discover", "Saved", "Reservations", "Profile"].map((item) => (
                <a 
                  key={item} 
                  href="#" 
                  className={`text-sm font-semibold transition-colors ${item === "Discover" ? "text-reco-red" : "text-text-secondary hover:text-reco-red"}`}
                >
                  {item}
                </a>
              ))}
            </nav>

            {/* Icons */}
            <div className="flex items-center gap-5 text-text-secondary">
              <Search size={20} className="hover:text-reco-red cursor-pointer transition-colors" />
              <Menu size={20} className="hover:text-reco-red cursor-pointer transition-colors" />
            </div>
          </div>
        </header>

        <main className="flex-grow">
          {children}
        </main>

        <footer className="bg-white border-t border-gray-100 py-12">
          <div className="container mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-2 text-reco-red font-black text-xl italic tracking-tight">
              <UtensilsCrossed size={24} />
              <span>Reco Partner</span>
            </div>
            
            <p className="text-sm text-text-muted">
              © {new Date().getFullYear()} Reco Partner. All rights reserved. Your ultimate dining companion.
            </p>

            <div className="flex items-center gap-6 text-sm font-medium text-text-secondary">
              <a href="#" className="hover:text-reco-red transition-colors">Terms</a>
              <a href="#" className="hover:text-reco-red transition-colors">Privacy</a>
              <a href="#" className="hover:text-reco-red transition-colors">Contact</a>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
