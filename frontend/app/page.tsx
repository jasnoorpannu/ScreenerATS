"use client";

import DarkModeToggle from "@/components/DarkModeToggle";

export default function Home() {
  return (
    <div className="min-h-screen w-full flex flex-col items-center justify-center bg-white text-black dark:bg-black dark:text-white transition-colors">
      
      {/* Dark Mode Switch */}
      <DarkModeToggle />

      <main className="flex flex-col items-center justify-center px-8 py-20 max-w-2xl w-full">
        
        {/* Title */}
        <h1 className="text-5xl font-semibold text-center tracking-tight mb-4">
          ATS Resume Scanner
        </h1>

        {/* Subtitle */}
        <p className="text-lg text-center max-w-xl text-zinc-600 dark:text-zinc-400 mb-10 leading-relaxed">
          Upload your resume and job description to generate a detailed ATS 
          score, keyword analysis, and LLM-based relevancy insights.
        </p>

        {/* CTA Button */}
        <a
          href="/analyze"
          className="flex h-12 items-center justify-center rounded-full 
                     bg-black text-white dark:bg-white dark:text-black 
                     px-10 text-lg font-medium shadow-md shadow-zinc-300/40 dark:shadow-none 
                     transition hover:opacity-80 hover:scale-[1.02]"
        >
          Get Started
        </a>
      </main>
    </div>
  );
}
