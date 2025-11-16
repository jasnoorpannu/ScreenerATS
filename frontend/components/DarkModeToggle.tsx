"use client";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";

export default function DarkModeToggle() {
  const [mounted, setMounted] = useState(false);
  const { theme, setTheme } = useTheme();

  // Only render after client-side hydration
  useEffect(() => {
    setMounted(true);
  }, []);

  // Prevent hydration mismatch by not rendering until mounted
  if (!mounted) {
    return (
      <button
        className="fixed top-4 right-4 px-4 py-2 rounded-lg 
                   bg-gray-200 dark:bg-[#222] text-black dark:text-white
                   shadow hover:scale-105 transition"
      >
        {/* Empty or a neutral icon */}
        ☀️
      </button>
    );
  }

  return (
    <button
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
      className="fixed top-4 right-4 px-4 py-2 rounded-lg 
                 bg-gray-200 dark:bg-[#222] text-black dark:text-white
                 shadow hover:scale-105 transition"
    >
      {theme === "dark" ? "🌞 Light Mode" : "🌙 Dark Mode"}
    </button>
  );
}