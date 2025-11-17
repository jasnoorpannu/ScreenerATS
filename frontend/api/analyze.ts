export async function analyzeResume(
  file: File,
  jobDescription: string,
  apiKey: string
) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('job_description', jobDescription);
  formData.append('api_key', apiKey);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://screenerats.onrender.com';

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 90000); // 90 second timeout

  try {
    const response = await fetch(`${API_URL}/analyze`, {
      method: 'POST',
      body: formData,
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Server error: ${response.status}`);
    }

    return await response.json();
  } catch (error: any) {
    clearTimeout(timeoutId);
    
    if (error.name === 'AbortError') {
      throw new Error('Request timeout. The server might be starting up. Please try again in 30 seconds.');
    } else if (error.message.includes('Failed to fetch')) {
      throw new Error('Cannot connect to server. Please wait 30 seconds and try again (server is waking up).');
    }
    throw error;
  }
}