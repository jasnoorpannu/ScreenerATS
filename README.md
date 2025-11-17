# ScreenerATS - AI-Powered Resume Analyzer

An intelligent ATS resume analyzer that helps optimize resumes for specific job descriptions using Google's Gemini AI.

## Features

- AI-powered resume analysis using Google Gemini
- Keyword matching with job descriptions
- Format and structure checking
- Comprehensive scoring breakdown
- Privacy-first: API keys are never stored

## Live Demo Site

https://screenerats.vercel.app

## Prerequisites

- Node.js (v18+)
- Python (v3.9+)
- Git
- Google Gemini API Key (free at https://aistudio.google.com/app/apikey)

## Local Setup

### Backend
```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs at http://localhost:8000

### Frontend
```bash
cd frontend
npm install

# Create .env.local file
echo "NEXT_PUBLIC_BACKEND_URL=http://localhost:8000" > .env.local

npm run dev
```

Frontend runs at http://localhost:3000

## How to Use

1. Get your free Gemini API key from https://aistudio.google.com/app/apikey
2. Navigate to the Analyze page
3. Upload your resume (PDF or DOCX)
4. Paste the job description
5. Enter your Gemini API key
6. Click "Analyze Resume"
7. View your results with detailed scoring

Note: First request may take 30-50 seconds as the server wakes up from sleep.

## Project Structure
```
ScreenerATS/
├── backend/
│   ├── services/          # Analysis modules
│   ├── main.py           # FastAPI app
│   └── requirements.txt
│
└── frontend/
    ├── app/              # Next.js pages
    ├── components/       # React components
    └── package.json
```

## Deployment

### Backend (Render)

1. Connect GitHub repository to Render
2. Configure:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)

1. Connect GitHub repository to Vercel
2. Configure:
   - Root Directory: `frontend`
   - Environment Variable: `NEXT_PUBLIC_BACKEND_URL=https://your-render-url.onrender.com`

## Troubleshooting

**502 Bad Gateway**: Server is waking up. Wait 30-50 seconds and retry.

**Analysis Failed**: Check your Gemini API key is valid and the file format is PDF or DOCX.

**CORS Errors**: Ensure your frontend URL is added to the backend's allowed origins in `main.py`.

## Tech Stack

- Backend: FastAPI, Python
- Frontend: Next.js, React, Tailwind CSS
- AI: Google Gemini API

## License

MIT License

## Contact

Developer: Jasnoor Pannu
GitHub: https://github.com/jasnoorpannu/ScreenerATS
