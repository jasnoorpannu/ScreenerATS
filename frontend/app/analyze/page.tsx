"use client";

import { useState } from "react";

export default function AnalyzePage() {
  const [file, setFile] = useState<File | null>(null);
  const [jobDesc, setJobDesc] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) setFile(e.target.files[0]);
  };

  const handleAnalyze = async () => {
    if (!file || !jobDesc.trim() || !apiKey.trim()) {
      alert("Upload resume, paste JD, and enter your Gemini API key.");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_description", jobDesc);
    formData.append("api_key", apiKey);

    try {
      const res = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      localStorage.setItem("ats-result", JSON.stringify(data));
      window.location.href = "/result";
    } catch (err) {
      alert("Something broke. Try again.");
    }

    setLoading(false);
  };

  return (
    <div
      className="
        min-h-screen flex flex-col items-center px-6 py-12 
        bg-gray-100 text-gray-900 
        dark:bg-black dark:text-white 
        transition-colors
      "
    >
      <h1 className="text-4xl font-bold mb-10 text-center">
        Analyze Your Resume
      </h1>

      <div
        className="
          w-full max-w-2xl 
          bg-white dark:bg-zinc-900 
          shadow-xl rounded-2xl p-8 
          border border-zinc-200 dark:border-zinc-800
          space-y-6
        "
      >
        {/* === Upload Resume === */}
        <div>
          <label
            className="
              block text-sm font-medium 
              text-gray-700 dark:text-gray-300 mb-2
            "
          >
            Upload Resume (PDF / DOCX)
          </label>
          <input
            type="file"
            accept=".pdf,.docx"
            onChange={handleUpload}
            className="
              w-full border border-gray-300 dark:border-zinc-700 
              rounded-md p-2 
              bg-white dark:bg-zinc-800 
              text-gray-900 dark:text-gray-100
            "
          />
        </div>

        {/* === Job Description === */}
        <div>
          <label
            className="
              block text-sm font-medium 
              text-gray-700 dark:text-gray-300 mb-2
            "
          >
            Paste Job Description
          </label>
          <textarea
            value={jobDesc}
            onChange={(e) => setJobDesc(e.target.value)}
            className="
              w-full border border-gray-300 dark:border-zinc-700 
              rounded-md p-3 h-48 resize-none
              bg-white dark:bg-zinc-800 
              text-gray-900 dark:text-gray-100
            "
            placeholder="Paste the job description here..."
          />
        </div>

        {/* === Gemini API Key === */}
        <div>
          <label
            className="
              block text-sm font-medium 
              text-gray-700 dark:text-gray-300 mb-2
            "
          >
            Your Gemini API Key
          </label>
          <input
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="AIza..."
            className="
              w-full border border-gray-300 dark:border-zinc-700 
              rounded-md p-2
              bg-white dark:bg-zinc-800 
              text-gray-900 dark:text-gray-100
            "
          />
        </div>

        {/* === Button === */}
        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="
            w-full py-3 rounded-lg text-lg font-semibold
            bg-blue-600 hover:bg-blue-700 text-white
            dark:bg-blue-500 dark:hover:bg-blue-600
            disabled:opacity-50
            transition
          "
        >
          {loading ? "Analyzing..." : "Analyze Resume"}
        </button>
      </div>
    </div>
  );
}
