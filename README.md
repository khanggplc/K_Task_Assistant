# AI Task Assistant 🚀

An intelligent task automation assistant integrating **Gmail**, **Zalo OA**, **Google Calendar**, and **AI parsing** to capture, evaluate, and schedule tasks automatically from messages and emails.

---

## 🌟 Key Features

1. **Multi-Channel Ingestion**:
   - **Gmail**: Webhook & push notifications via Google Cloud Pub/Sub, message fetching and parsing.
   - **Zalo OA**: Real-time webhook listener and automated messaging.
2. **AI Action Engine**:
   - Extract actionable tasks, dates, priorities, and assignees using LLMs.
   - Smart intent evaluator: distinguishes casual conversations from concrete commitments.
3. **Execution & Syncing**:
   - Syncs scheduled events to **Google Calendar**.
   - Confirmation workflows: requests user approval before final booking.
   - Automated reminders and overdue task tracking.
4. **Reliable Background Workers**:
   - Asynchronous message queueing and periodic polling via APScheduler / workers.

---

## 🏗️ Architecture & Structure

```
ai-task-assistant/
├── app/
│   ├── main.py                     # Application entry point & FastAPI setup
│   ├── core/                       # App configuration, security, and logging
│   ├── api/                        # REST & Webhook routes
│   ├── integrations/               # External APIs (Gmail, Zalo, Calendar)
│   ├── ai/                         # LLM prompts, parsing, evaluator, schemas
│   ├── models/                     # SQLAlchemy 2.0 ORM models
│   ├── repositories/               # Data access layer
│   ├── services/                   # Business logic (tasks, messages, reminders)
│   ├── workers/                    # Background workers & scheduler
│   └── db/                         # Database session, migrations, seeding
├── tests/                          # Unit and integration test suites
├── scripts/                        # Utility & operational scripts
├── data/                           # Local storage (SQLite, temp files)
└── frontend/                       # Web UI dashboard
```

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.10+
- Virtualenv or Conda
- Docker (optional)

### 2. Setup Environment
```bash
# Clone and enter directory
cd ai-task-assistant

# Create virtual environment
python -m venv .venv
# Activate:
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"
```

### 3. Configure `.env`
```bash
cp .env.example .env
# Fill in your AI API key and OAuth credentials
```

### 4. Run Application
```bash
uvicorn app.main:app --reload --port 8000
```
Visit API Documentation at [http://localhost:8000/docs](http://localhost:8000/docs).
