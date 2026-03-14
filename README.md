# StartupMetrics - Unit Economics & Runway Dashboard

AI-powered unit economics dashboard for startup founders. Track CAC, LTV, Burn Rate, and Runway with beautiful visualizations and AI-generated insights.

## Features

- **CAC Analysis** - Customer Acquisition Cost by channel, campaign, and platform
- **LTV Analysis** - Lifetime Value by income segments and age groups
- **Burn Rate** - Monthly expense vs revenue tracking
- **Runway Prediction** - Cash runway with what-if scenarios
- **AI Financial Advisor** - Chat with AI about your startup finances
- **Beautiful Dashboard** - Modern SaaS-style dark theme UI

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, TailwindCSS, Framer Motion |
| Backend | Python FastAPI |
| Database | PostgreSQL |
| Data Processing | Pandas |
| AI | Ollama (local LLM) |
| Auth | JWT + Bcrypt |

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 16+
- Ollama

### Backend Setup

```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
