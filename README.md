<div align="center">

# 📦 InventoryAIgent
### Intelligent ERP Knowledge Assistant

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-19.2-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-7.2-646CFF?style=flat-square&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Flask](https://img.shields.io/badge/Flask-black?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

Agentic AI platform for automating inventory analysis and financial auditing for SMEs using Tally ERP exports.

[Overview](#overview) • [Quick Start](#quick-start) • [Key Features](#key-features) • [System Architecture](#system-architecture) • [AI Agents](#ai-agents) • [Repository Structure](#repository-structure) • [API Endpoints (High Level)](#api-endpoints-high-level) • [Database Schema](#database-schema) • [Tech Stack](#tech-stack) • [Setup](#setup) • [Run Locally](#run-locally) • [Typical Workflow](#typical-workflow) 

[Inventory_Agent - Comprehensive Codebase Analysis](#inventory_agent---comprehensive-codebase-analysis) • [Project Overview & Purpose](#1-project-overview--purpose) • [Architecture Overview](#2-architecture-overview) • [Key Files and Their Responsibilities](#3-key-files-and-their-responsibilities) • [The "Agentic AI" Aspect - All 7 Agents](#4-the-agentic-ai-aspect---all-7-agents) • [Database Schema (inventory.db)](#5-database-schema-inventorydb) • [Frontend Structure (React + Vite)](#6-frontend-structure-react--vite) • [Dependencies & How to Run](#7-dependencies--how-to-run) • [Data Flow Example](#8-data-flow-example) • [Documentation Summary from AgenticAIProject.txt](#9-documentation-summary-from-agenticaiaprojecttxt) • [Summary of Technologies Used](#10-summary-of-technologies-used)

</div>

# Overview

Agentic AI platform for inventory analysis and financial auditing, built for SMEs using Tally ERP exports.

This project combines a Flask backend, React frontend, SQLite storage, and CrewAI multi-agent orchestration to turn spreadsheet data into natural-language business insights.

## Quick Start

```bash
# 1) Backend (from project root)
source .venv/bin/activate
python app.py

# 2) Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Open:

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:5000`

Required env var in `.env`:

```env
GROQ_API_KEY=your_api_key 
```
## Key Features

- Upload stock summary files and run automated inventory analysis
- Generate executive-readable AI reports from raw stock data
- View real-time agent reasoning logs with SSE streaming
- Track historical runs and compare inventory health over time
- Query inventory data using natural language (NL to SQL)
- Forecast stock depletion trends with ML-based predictions
- Send low-stock and critical-stock reorder email alerts
- Audit ledger files for financial risks and compliance anomalies

## System Architecture

The application is organized as:

- **Frontend**: React + Vite dashboard with analysis, chat, history, forecast, and audit pages
- **Backend**: Flask REST API with modular route blueprints
- **Agent Layer**: CrewAI agents with specialized tools
- **Data Layer**: SQLite database (`inventory.db`) for run history and item snapshots

## AI Agents

1. **Stock Analyst** - Parses inventory files and classifies stock status
2. **Business Reporter** - Converts analysis output into business summaries
3. **Comparison Analyst** - Compares two historical runs and explains trends
4. **Data Analyst** - Answers questions from database data using SQL tools
5. **Demand Forecaster** - Predicts item stock-out trends
6. **Purchasing Manager** - Triggers reorder workflows and email alerts
7. **Financial Auditor** - Reviews ledger inputs for risky patterns

## Repository Structure

```text
Inventory_Agent/
├── app.py                      # Flask app entrypoint and setup
├── main.py                     # Standalone CrewAI run entrypoint
├── inventory.db                # SQLite database
├── .env                        # Environment variables
├── src/
│   ├── agents.py               # Agent definitions and tool assignment
│   ├── tasks.py                # CrewAI task definitions
│   ├── tools.py                # Core inventory analysis tool
│   ├── db.py                   # DB setup and CRUD helpers
│   ├── llm_config.py           # LLM provider/model configuration
│   ├── stream_capture.py       # Agent log capture for SSE
│   ├── query_tool.py           # NL-to-SQL query tools
│   ├── forecast_tool.py        # Forecasting logic
│   ├── email_tool.py           # SMTP/Gmail alert sender
│   ├── audit_tool.py           # Ledger audit utilities
│   └── routes/
│       ├── upload.py           # Upload and streaming endpoints
│       ├── results.py          # Results and report download endpoints
│       ├── history.py          # History and comparison endpoints
│       ├── chat.py             # Query endpoint
│       ├── alerts.py           # Alert endpoint
│       ├── forecast.py         # Forecast endpoints
│       └── audit.py            # Audit endpoint
├── frontend/
│   ├── src/components/         # Layout, sidebar, logs, storyboard
│   └── src/pages/              # Analyze, dashboard, history, chat, audit
├── data/                       # Uploaded/working data files
└── reports/                    # Generated report files
```

## API Endpoints (High Level)

- `POST /upload` - Upload and analyze stock file
- `POST /upload-stream` - Upload with live SSE agent logs
- `GET /results/<run_id>` - Fetch a specific run result
- `GET /history` - List previous analysis runs
- `GET /compare` - Compare two runs
- `POST /query` - Natural language query endpoint
- `GET /forecast` and `GET /forecast/top` - Forecast outputs
- `POST /alerts/send` - Send stock alerts
- `POST /audit/upload` - Upload ledger for audit

## Database Schema

The SQLite database has two primary tables:

- `analysis_runs`: run metadata, status, summary counts, and agent output
- `analysis_items`: per-item snapshot records linked to a run (`run_id`)

## Tech Stack

- **AI/Orchestration**: CrewAI, LiteLLM, Groq-hosted LLaMA model
- **Backend**: Flask, Flask-CORS, Python
- **Data Processing**: pandas, openpyxl
- **Machine Learning**: scikit-learn
- **Frontend**: React, React Router, Vite, Axios
- **Visualization**: Recharts
- **Storage**: SQLite

## Setup

### Prerequisites

- Python 3.12+ (project includes `.venv`)
- Node.js 18+ and npm
- Groq API key

### Environment Variables

Create/update `.env` in project root:

```env
GROQ_API_KEY=your_groq_api_key
FLASK_SECRET_KEY=your_secret_key
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
```

`GROQ_API_KEY` is required for agent execution. Gmail values are needed only for email alerts.

## Run Locally

### 1) Start Backend

```bash
source .venv/bin/activate
python app.py
```

Backend starts on `http://localhost:5000` (default).

### 2) Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend starts on Vite default port (typically `http://localhost:5173`).

### 3) Optional: Run Agents via CLI

```bash
python main.py
```

## Typical Workflow

1. Upload Tally stock summary file from the Analyze page
2. Watch live agent logs as Stock Analyst and Reporter complete tasks
3. Review categorized inventory health and generated business report
4. Explore dashboard charts and forecast outputs
5. Use history/compare to evaluate trends across runs
6. Trigger alerts or run ledger audits as needed


# Inventory_Agent - Comprehensive Codebase Analysis

## 1. Project Overview & Purpose

InventoryAIgent is an Agentic AI platform for automating inventory analysis and financial auditing for SMEs using Tally ERP. This is an MCA Final Year Project (20-credit) that demonstrates the application of Multi-Agent Systems (MAS) to enterprise resource planning.

### Key Value Proposition
- **Data Transformation:** Transforms raw Tally ERP exports (Excel files) into actionable business insights.
- **Agentic AI:** Uses autonomous AI agents that collaborate to perform complex reasoning.
- **Actionable Insights:** Provides natural language summaries instead of static Excel reports.
- **Transparent Processing:** Shows the AI's "thought process" in real-time for transparency.

---

## 2. Architecture Overview

```text
┌─────────────────────────────────────────────────────────────────┐
│                     FRONTEND (React + Vite)                     │
│  ┌─────────┐ ┌───────────┐ ┌─────────┐ ┌──────┐ ┌───────┐       │
│  │ Analyze │ │ Dashboard │ │ History │ │ Chat │ │ Audit │       │
│  └────┬────┘ └─────┬─────┘ └────┬────┘ └───┬──┘ └───┬───┘       │
└───────┼────────────┼────────────┼──────────┼────────┼───────────┘
        │            │            │          │        │
        │       REST API / SSE (Server-Sent Events)   │
        │            │            │          │        │
┌───────┼────────────┼────────────┼──────────┼────────┼───────────┐
│       ▼            ▼            ▼          ▼        ▼           │
│                     BACKEND (Flask)                             │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  Routes: /upload, /results, /history, /query,        │       │
│  │          /alerts, /forecast, /audit, /compare        │       │
│  └──────────────────────────────────────────────────────┘       │
│                           │                                     │
│                     CrewAI Engine                               │
│  ┌──────────────────────────────────────────────────────┐       │
│  │           MULTI-AGENT ORCHESTRATION                  │       │
│  │  ┌───────────────┐  ┌──────────────────┐             │       │
│  │  │ Stock Analyst │──│ Business Reporter│             │       │
│  │  └───────────────┘  └──────────────────┘             │       │
│  │  ┌───────────────┐  ┌──────────────────┐             │       │
│  │  │ Data Analyst  │  │  Forecast Agent  │             │       │
│  │  └───────────────┘  └──────────────────┘             │       │
│  │  ┌───────────────┐  ┌──────────────────┐             │       │
│  │  │ Reorder Agent │  │   Audit Agent    │             │       │
│  │  └───────────────┘  └──────────────────┘             │       │
│  │  ┌────────────────┐                                  │       │
│  │  │Comparison Agent│                                  │       │
│  │  └────────────────┘                                  │       │
│  └──────────────────────────────────────────────────────┘       │
│                           │                                     │
│  ┌──────────┐  ┌─────────────────────────────────────────┐      │
│  │ SQLite   │  │              AGENT TOOLS                │      │
│  │ Database │  │  - Inventory Analysis Tool              │      │
│  │          │  │  - SQL Query Tool                       │      │
│  │          │  │  - Forecast Tool (sklearn)              │      │
│  │          │  │  - Email Alert Tool                     │      │
│  │          │  │  - Ledger Audit Tool                    │      │
│  └──────────┘  └─────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
``` 
## 3. Key Files and Their Responsibilities

### Backend Core Files

*   `**/app.py**`: Flask application factory with CORS, blueprint registration, database initialization
    
*   `**/main.py**`: Standalone CLI entry point to run CrewAI agents directly (without web interface)
    
*   `**/src/agents.py**`: Defines all 7 AI agents with their roles, goals, backstories, and tools
    
*   `**/src/tasks.py**`: Defines CrewAI tasks (analysis\_task, reporting\_task)
    
*   `**/src/tools.py**`: Core inventory analysis tool using pandas to process Tally Excel exports
    
*   `**/src/db.py**`: SQLite database operations (save runs, get history, compare runs)
    
*   `**/src/llm\_config.py**`: LLM configuration - uses Groq's LLaMA 3.1-8B (free tier) via CrewAI
    
*   `**/src/stream\_capture.py**`: Captures CrewAI verbose output and streams it as SSE events for real-time UI
    

### Tool Modules

*   `**/src/query\_tool.py**`: Natural language to SQL translation for querying inventory database
    
*   `**/src/forecast\_tool.py**`: Linear regression forecasting using scikit-learn
    
*   `**/src/email\_tool.py**`: SMTP email alerting via Gmail
    
*   `**/src/audit\_tool.py**`: Financial ledger analysis for risk detection
    

### Route Modules (/src/routes/)

*   `**upload.py**`: POST /upload, POST /upload-stream (SSE)
    
*   `**results.py**`: GET /results/, GET /download/
    
*   `**history.py**`: GET /history, GET /compare
    
*   `**chat.py**`: POST /query
    
*   `**alerts.py**`: POST /alerts/send
    
*   `**forecast.py**`: GET /forecast, GET /forecast/top
    
*   `**audit.py**`: POST /audit/upload


## 4. The "Agentic AI" Aspect - All 7 Agents

### Agent 1: **Stock Analyst** (`stock_analyst_agent`)
- **Role**: Inventory Analyst
- **Tool**: `inventory_analysis_tool`
- **Function**: Processes Tally Excel exports, identifies out-of-stock, low-stock, and critical (negative balance) items

### Agent 2: **Business Reporter** (`report_creator_agent`)
- **Role**: Business Reporter
- **Tool**: None (uses context from Agent 1)
- **Function**: Transforms technical analysis into executive-friendly natural language summaries

### Agent 3: **Comparison Analyst** (`comparison_analyst`)
- **Role**: Inventory Comparison Analyst
- **Tool**: None
- **Function**: Compares two analysis snapshots and generates narratives about inventory health trends

### Agent 4: **Data Analyst** (`data_analyst_agent`)
- **Role**: Inventory Data Analyst
- **Tools**: `get_database_schema`, `execute_sql_query`
- **Function**: Answers natural language questions by translating to SQL and querying the database

### Agent 5: **Demand Forecaster** (`forecast_agent`)
- **Role**: Inventory Demand Forecaster
- **Tool**: `forecast_item_tool`
- **Function**: Uses linear regression to predict when items will run out of stock

### Agent 6: **Purchasing Manager** (`reorder_agent`)
- **Role**: Purchasing Manager
- **Tool**: `send_email_alert`
- **Function**: Generates and sends reorder alerts for critical stock items

### Agent 7: **Financial Auditor** (`audit_agent`)
- **Role**: Financial Compliance Auditor
- **Tool**: `analyze_ledger_tool`
- **Function**: Analyzes ledger files for high-value transactions, missing data, and compliance risks
---

## 5. Database Schema (inventory.db)

SQLite database with 2 tables:

### Table: analysis_runs

```text
CREATE TABLE analysis_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    input_filename TEXT NOT NULL,
    report_filename TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    agent_output TEXT,           -- Raw agent text output
    summary_json TEXT,           -- JSON with detailed stats
    out_of_stock_count INTEGER DEFAULT 0,
    low_stock_count INTEGER DEFAULT 0,
    critical_count INTEGER DEFAULT 0,
    total_items INTEGER DEFAULT 0
);
```

### Table: analysis_items

```text
CREATE TABLE analysis_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    item_name TEXT NOT NULL,
    closing_balance REAL NOT NULL,
    category TEXT NOT NULL,      -- 'out_of_stock', 'low_stock', 'critical'
    FOREIGN KEY (run_id) REFERENCES analysis_runs(id)
);
```
---

## 6. Frontend Structure (React + Vite)

### Technology Stack
- React 19.2 with React Router DOM 7.14
- Vite 7.2 for build tooling
- Recharts 3.8 for data visualization
- Axios for HTTP requests
- Lucide React for icons
- React Markdown for rendering AI responses

### Component Architecture

```text
frontend/src/
├── main.jsx              # App entry point
├── App.jsx               # Router configuration with 5 routes
├── index.css             # Global styles
├── components/
│   ├── Layout.jsx        # Sidebar + main content wrapper
│   ├── Sidebar.jsx       # Navigation with 5 menu items
│   ├── StoryBoard.jsx    # Visual agent pipeline (Analyst→Reporter→Ready)
│   └── AgentLog.jsx      # Real-time agent thought process viewer
└── pages/
    ├── AnalyzePage.jsx   # File upload with SSE streaming
    ├── DashboardPage.jsx # Charts, stats, forecasts, alerts
    ├── HistoryPage.jsx   # Timeline of past analyses with comparison
    ├── ChatPage.jsx      # Natural language query interface
    └── AuditPage.jsx     # Ledger audit file upload
```

### Key UI Features
- StoryBoard Component: Visualizes the agent pipeline (Stock Analyst → Business Reporter → Ready)
- AgentLog Component: Real-time streaming of agent thoughts via SSE
- Dashboard: Pie charts (stock health), bar charts (critical items), line charts (forecasts)
- History Comparison: Select two runs and generate AI-powered narrative comparison
---

## 7. Dependencies & How to Run

### Backend Dependencies (Python)
The project uses a Python virtual environment (.venv/) with key packages:
- crewai - Multi-agent orchestration framework
- flask + flask-cors - REST API
- pandas + openpyxl - Excel processing
- scikit-learn - Linear regression for forecasting
- python-dotenv - Environment variable management
- litellm - LLM abstraction layer

### Frontend Dependencies
From package.json:
- react, react-dom, react-router-dom
- recharts (charting)
- axios (HTTP client)
- lucide-react (icons)
- react-markdown
- vite (dev server/bundler)

### Environment Variables Required (.env)
```text
GROQ_API_KEY=<your-groq-api-key>      - Required for LLM
FLASK_SECRET_KEY=<secret>             - Optional
GMAIL_USER=<email>                    - Optional for email alerts
GMAIL_APP_PASSWORD=<app-password>     - Optional for email alerts
```
### Running the Project

#### Backend:
```text
cd /Users/yash/Inventory_Agent
source .venv/bin/activate
python app.py   # Starts Flask on port 5000
```
#### Frontend:
```text
cd /Users/yash/Inventory_Agent/frontend
npm install     # If first time
npm run dev     # Starts Vite dev server (usually port 5173)
```
#### Standalone CLI (without web):
```text
python main.py  # Runs CrewAI agents directly
```
---

## 8. Data Flow Example

1. **User uploads** `Stock_Summary_2026-04-07.xlsx` via frontend
2. **Frontend** sends to `/upload-stream` (SSE endpoint)
3. **Backend** saves file to `/data/`, starts CrewAI crew
4. **Stock Analyst Agent** uses `inventory_analysis_tool` to:
   - Parse Excel, clean numeric columns
   - Categorize items: Out of Stock (balance=0), Low Stock (<5), Critical (<0)
   - Generate Excel report in `/reports/`
5. **Business Reporter Agent** receives context, writes executive summary
6. **Stream Capture** sends agent thoughts to frontend via SSE
7. **Results saved** to SQLite database with item-level detail
8. **Frontend Dashboard** shows pie charts, tables, and the AI summary
---

## 9. Documentation Summary from AgenticAIProject.txt

This file serves as the project proposal/technical document for academic submission:

- Target Users: SMEs using Tally Prime ERP
- Problem Solved: Data overload, manual report generation, static reporting
- Current Implementation: Stock analysis with categorization logic
- Future Roadmap (proposed for full 20-credit project):
  - Phase 2: Debtor Aging Analysis, Cash Flow Prediction, GST Compliance
  - Phase 3: "Chat with Tally" using RAG
  - Phase 4: Anomaly Detection for unusual ledger entries
- Research Questions: CrewAI vs Hierarchical agents, hallucination mitigation, data privacy
---

## 10. Summary of Technologies Used
---------------------------------

*   **LLM:** Groq LLaMA 3.1-8B (via CrewAI + LiteLLM)
    
*   **Agent Framework:** CrewAI (sequential process)
    
*   **Backend:** Flask + Flask-CORS
    
*   **Database:** SQLite
    
*   **Data Processing:** Pandas + OpenPyXL
    
*   **ML/Forecasting:** scikit-learn (LinearRegression)
    
*   **Frontend:** React 19 + Vite + React Router
    
*   **Visualization:** Recharts
    
*   **Real-time Streaming:** Server-Sent Events (SSE)
    
*   **Email:** smtplib (Gmail SMTP)


