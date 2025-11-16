"use client";

import { useEffect, useState } from "react";
import ScoreRing from "@/components/ScoreRing";

export default function ResultPage() {
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    const stored = localStorage.getItem("ats-result");
    if (stored) setResult(JSON.parse(stored));
  }, []);

  if (!result) {
    return (
      <div className="min-h-screen flex items-center justify-center 
                      text-gray-700 dark:text-gray-300
                      bg-gray-100 dark:bg-black">
        No data found. Please analyze a resume first.
      </div>
    );
  }

  const { final_score, score_breakdown, keywords, formatting } = result;

  return (
    <div className="min-h-screen py-10 px-4 flex flex-col items-center 
                    bg-gray-100 text-gray-900 
                    dark:bg-black dark:text-white transition-colors">
      
      {/* TITLE */}
      <h1 className="text-4xl font-bold mb-10">ATS Score Report</h1>

      <div className="w-full max-w-3xl space-y-10">

        {/* SCORE CARD */}
        <div className="bg-white dark:bg-zinc-900 
                        shadow-lg rounded-2xl p-8 flex flex-col items-center
                        border border-zinc-200 dark:border-zinc-800">

          <ScoreRing score={final_score} />
          <p className="text-lg text-gray-600 dark:text-gray-400 mt-4">
            ATS Compatibility Score
          </p>
        </div>

        {/* SCORE BREAKDOWN */}
        <div className="bg-white dark:bg-zinc-900 
                        shadow-lg rounded-2xl p-8
                        border border-zinc-200 dark:border-zinc-800">

          <h2 className="text-2xl font-semibold mb-4">Score Breakdown</h2>

          <div className="grid grid-cols-2 gap-y-3 text-gray-700 dark:text-gray-300">
            <p><strong>Relevancy Score:</strong> {score_breakdown.relevancy_score}</p>
            <p><strong>Skill Strength:</strong> {score_breakdown.skill_strength}</p>
            <p><strong>Experience Strength:</strong> {score_breakdown.experience_strength}</p>
            <p><strong>Keyword Score:</strong> {score_breakdown.keyword_score}</p>
            <p><strong>Formatting Score:</strong> {score_breakdown.format_score}</p>
          </div>
        </div>

        {/* KEYWORD SECTION */}
        <div className="bg-white dark:bg-zinc-900 
                        shadow-lg rounded-2xl p-8
                        border border-zinc-200 dark:border-zinc-800">

          <h2 className="text-2xl font-semibold mb-4">Keyword Analysis</h2>

          {/* MATCHED */}
          <div className="mb-6">
            <h3 className="font-medium text-gray-800 dark:text-gray-300">
              Matched Keywords
            </h3>
            <div className="flex flex-wrap gap-2 mt-2">
              {keywords.matched.length ? (
                keywords.matched.map((kw: string, i: number) => (
                  <span key={i}
                    className="px-3 py-1 bg-green-200 dark:bg-green-900 
                               text-green-800 dark:text-green-200 
                               rounded-full text-sm">
                    {kw}
                  </span>
                ))
              ) : (
                <p className="text-gray-500 dark:text-gray-400 text-sm">
                  None matched.
                </p>
              )}
            </div>
          </div>

          {/* MISSING */}
          <div>
            <h3 className="font-medium text-gray-800 dark:text-gray-300">
              Missing Keywords
            </h3>
            <div className="flex flex-wrap gap-2 mt-2">
              {keywords.missing.length ? (
                keywords.missing.map((kw: string, i: number) => (
                  <span key={i}
                    className="px-3 py-1 bg-red-200 dark:bg-red-900 
                               text-red-800 dark:text-red-200 
                               rounded-full text-sm">
                    {kw}
                  </span>
                ))
              ) : (
                <p className="text-gray-500 dark:text-gray-400 text-sm">
                  None missing.
                </p>
              )}
            </div>
          </div>

        </div>

        {/* FORMATTING SECTION */}
        <div className="bg-white dark:bg-zinc-900 
                        shadow-lg rounded-2xl p-8
                        border border-zinc-200 dark:border-zinc-800">

          <h2 className="text-2xl font-semibold mb-4">
            Formatting & Structure
          </h2>

          <ul className="space-y-2 text-gray-700 dark:text-gray-300">
            <li><strong>Sections Detected:</strong> {formatting.sections}</li>
            <li><strong>Bullet Points:</strong> {formatting.bullets}</li>
            <li><strong>Average Line Length:</strong> {formatting.avg_line_length}</li>
            <li><strong>Headings Found:</strong> {formatting.has_headings ? "Yes" : "No"}</li>
            <li><strong>Formatting Score:</strong> {score_breakdown.format_score}</li>
          </ul>
        </div>

      </div>
    </div>
  );
}
