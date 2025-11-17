"use client";
import { useState } from "react";

export default function AnalyzePage() {
  const [file, setFile] = useState<File | null>(null);
  const [jobDesc, setJobDesc] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) setFile(e.target.files[0]);
  };

  const handleAnalyze = async () => {
    if (!file || !jobDesc.trim() || !apiKey.trim()) {
      setError("Please upload resume, paste job description, and enter your Gemini API key.");
      return;
    }

    setLoading(true);
    setError(null);
    setStatus("Uploading resume and analyzing... This may take 30-50 seconds on first request (server waking up).");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_description", jobDesc);
    formData.append("api_key", apiKey);

    const backendRoot =
      process.env.NEXT_PUBLIC_BACKEND_URL || "https://screenerats.onrender.com";

    // Create abort controller for timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 90000); // 90 second timeout

    try {
      const res = await fetch(`${backendRoot}/analyze`, {
        method: "POST",
        body: formData,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!res.ok) {
        const txt = await res.text();
        console.error("Backend error:", txt);
        throw new Error(`Analysis failed: ${res.status} ${res.statusText}`);
      }

      const data = await res.json();
      localStorage.setItem("ats-result", JSON.stringify(data));
      setStatus("Analysis complete! Redirecting...");
      
      // Small delay before redirect for better UX
      setTimeout(() => {
        window.location.href = "/result";
      }, 500);

    } catch (err: any) {
      clearTimeout(timeoutId);
      console.error(err);
      
      if (err.name === 'AbortError') {
        setError("Request timeout. The server might be starting up. Please wait 30 seconds and try again.");
      } else if (err.message.includes('Failed to fetch')) {
        setError("Cannot connect to server. Please wait 30 seconds and try again (server is waking up from sleep).");
      } else {
        setError(err.message || "Network or server error. Check console for details.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center px-6 py-12 bg-gray-100 text-gray-900 dark:bg-black dark:text-white transition-colors">
      <h1 className="text-4xl font-bold mb-10 text-center">Analyze Your Resume</h1>
      
      <div className="w-full max-w-2xl bg-white dark:bg-zinc-900 shadow-xl rounded-2xl p-8 border border-zinc-200 dark:border-zinc-800 space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Upload Resume (PDF / DOCX)
          </label>
          <input
            type="file"
            accept=".pdf,.docx"
            onChange={handleUpload}
            disabled={loading}
            className="w-full border border-gray-300 dark:border-zinc-700 rounded-md p-2 bg-white dark:bg-zinc-800 text-gray-900 dark:text-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Paste Job Description
          </label>
          <textarea
            value={jobDesc}
            onChange={(e) => setJobDesc(e.target.value)}
            disabled={loading}
            className="w-full border border-gray-300 dark:border-zinc-700 rounded-md p-3 h-48 resize-none bg-white dark:bg-zinc-800 text-gray-900 dark:text-gray-100 disabled:opacity-50"
            placeholder="Paste the job description here..."
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Your Gemini API Key
          </label>
          <input
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            disabled={loading}
            placeholder="Enter your Gemini API key (kept local)"
            className="w-full border border-gray-300 dark:border-zinc-700 rounded-md p-2 bg-white dark:bg-zinc-800 text-gray-900 dark:text-gray-100 disabled:opacity-50"
          />
          <p className="mt-2 text-xs text-gray-500 dark:text-gray-400">
            We use this key just for the current analysis and do not store it.{' '}
            <a 
              href="https://aistudio.google.com/app/apikey" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline"
            >
              Get your free API key here
            </a>
          </p>
        </div>

        {/* Status message */}
        {status && (
          <div className="p-4 bg-blue-100 dark:bg-blue-900 border border-blue-300 dark:border-blue-700 rounded-md">
            <p className="text-sm text-blue-800 dark:text-blue-200">{status}</p>
          </div>
        )}

        {/* Error message */}
        {error && (
          <div className="p-4 bg-red-100 dark:bg-red-900 border border-red-300 dark:border-red-700 rounded-md">
            <p className="text-sm text-red-800 dark:text-red-200">{error}</p>
          </div>
        )}

        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="w-full py-3 rounded-lg text-lg font-semibold bg-blue-600 hover:bg-blue-700 text-white dark:bg-blue-500 dark:hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition"
        >
          {loading ? "Analyzing..." : "Analyze Resume"}
        </button>

        {/* Info box about cold starts */}
        <div className="mt-4 p-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-md">
          <p className="text-xs text-yellow-800 dark:text-yellow-200">
            ℹ️ <strong>First-time users:</strong> The server may take 30-50 seconds to wake up on the first request. Subsequent requests will be faster.
          </p>
        </div>
      </div>
    </div>
  );
}