
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
│  │  ┌───────────────┐  ┌─────────────────┐              │       │
│  │  │ Stock Analyst │──│ Business Reporter│              │       │
│  │  └───────────────┘  └─────────────────┘              │       │
│  │  ┌───────────────┐  ┌─────────────────┐              │       │
│  │  │ Data Analyst  │  │ Forecast Agent  │              │       │
│  │  └───────────────┘  └─────────────────┘              │       │
│  │  ┌───────────────┐  ┌─────────────────┐              │       │
│  │  │ Reorder Agent │  │ Audit Agent     │              │       │
│  │  └───────────────┘  └─────────────────┘              │       │
│  │  ┌───────────────┐                                   │       │
│  │  │Comparison Agent│                                  │       │
│  │  └───────────────┘                                   │       │
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
└─────────────────────────────────────────────────────────────────┘3\. Key Files and Their Responsibilities
----------------------------------------

### Backend Core Files

*   **/app.py**: Flask application factory with CORS, blueprint registration, database initialization
    
*   **/main.py**: Standalone CLI entry point to run CrewAI agents directly (without web interface)
    
*   **/src/agents.py**: Defines all 7 AI agents with their roles, goals, backstories, and tools
    
*   **/src/tasks.py**: Defines CrewAI tasks (analysis\_task, reporting\_task)
    
*   **/src/tools.py**: Core inventory analysis tool using pandas to process Tally Excel exports
    
*   **/src/db.py**: SQLite database operations (save runs, get history, compare runs)
    
*   **/src/llm\_config.py**: LLM configuration - uses Groq's LLaMA 3.1-8B (free tier) via CrewAI
    
*   **/src/stream\_capture.py**: Captures CrewAI verbose output and streams it as SSE events for real-time UI
    

### Tool Modules

*   **/src/query\_tool.py**: Natural language to SQL translation for querying inventory database
    
*   **/src/forecast\_tool.py**: Linear regression forecasting using scikit-learn
    
*   **/src/email\_tool.py**: SMTP email alerting via Gmail
    
*   **/src/audit\_tool.py**: Financial ledger analysis for risk detection
    

### Route Modules (/src/routes/)

*   **upload.py**: POST /upload, POST /upload-stream (SSE)
    
*   **results.py**: GET /results/, GET /download/
    
*   **history.py**: GET /history, GET /compare
    
*   **chat.py**: POST /query
    
*   **alerts.py**: POST /alerts/send
    
*   **forecast.py**: GET /forecast, GET /forecast/top
    
*   **audit.py**: POST /audit/upload
    

4\. The "Agentic AI" Aspect - All 7 Agents
------------------------------------------

### Agent 1: Stock Analyst (stock\_analyst\_agent)

*   **Role:** Inventory Analyst
    
*   **Tool:** inventory\_analysis\_tool
    
*   **Function:** Processes Tally Excel exports, identifies out-of-stock, low-stock, and critical (negative balance) items
    

### Agent 2: Business Reporter (report\_creator\_agent)

*   **Role:** Business Reporter
    
*   **Tool:** None (uses context from Agent 1)
    
*   **Function:** Transforms technical analysis into executive-friendly natural language summaries
    

### Agent 3: Comparison Analyst (comparison\_analyst)

*   **Role:** Inventory Comparison Analyst
    
*   **Tool:** None
    
*   **Function:** Compares two analysis snapshots and generates narratives about inventory health trends
    

### Agent 4: Data Analyst (data\_analyst\_agent)

*   **Role:** Inventory Data Analyst
    
*   **Tools:** get\_database\_schema, execute\_sql\_query
    
*   **Function:** Answers natural language questions by translating to SQL and querying the database
    

### Agent 5: Demand Forecaster (forecast\_agent)

*   **Role:** Inventory Demand Forecaster
    
*   **Tool:** forecast\_item\_tool
    
*   **Function:** Uses linear regression to predict when items will run out of stock
    

### Agent 6: Purchasing Manager (reorder\_agent)

*   **Role:** Purchasing Manager
    
*   **Tool:** send\_email\_alert
    
*   **Function:** Generates and sends reorder alerts for critical stock items
    

### Agent 7: Financial Auditor (audit\_agent)

*   **Role:** Financial Compliance Auditor
    
*   **Tool:** analyze\_ledger\_tool
    
*   **Function:** Analyzes ledger files for high-value transactions, missing data, and compliance risks
    

5\. Database Schema (inventory.db)
----------------------------------

SQLite database with 2 tables:

### Table: analysis\_runs

SQL

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   CREATE TABLE analysis_runs (      id INTEGER PRIMARY KEY AUTOINCREMENT,      timestamp TEXT NOT NULL,      input_filename TEXT NOT NULL,      report_filename TEXT,      status TEXT NOT NULL DEFAULT 'pending',      agent_output TEXT,           -- Raw agent text output      summary_json TEXT,           -- JSON with detailed stats      out_of_stock_count INTEGER DEFAULT 0,      low_stock_count INTEGER DEFAULT 0,      critical_count INTEGER DEFAULT 0,      total_items INTEGER DEFAULT 0  );   `

### Table: analysis\_items

SQL

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   CREATE TABLE analysis_items (      id INTEGER PRIMARY KEY AUTOINCREMENT,      run_id INTEGER NOT NULL,      item_name TEXT NOT NULL,      closing_balance REAL NOT NULL,      category TEXT NOT NULL,      -- 'out_of_stock', 'low_stock', 'critical'      FOREIGN KEY (run_id) REFERENCES analysis_runs(id)  );   `

6\. Frontend Structure (React + Vite)
-------------------------------------

### Technology Stack

*   **React 19.2** with React Router DOM 7.14
    
*   **Vite 7.2** for build tooling
    
*   **Recharts 3.8** for data visualization
    
*   **Axios** for HTTP requests
    
*   **Lucide React** for icons
    
*   **React Markdown** for rendering AI responses
    

### Component Architecture

Plaintext

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   frontend/src/  ├── main.jsx              # App entry point  ├── App.jsx               # Router configuration with 5 routes  ├── index.css             # Global styles  ├── components/  │   ├── Layout.jsx        # Sidebar + main content wrapper  │   ├── Sidebar.jsx       # Navigation with 5 menu items  │   ├── StoryBoard.jsx    # Visual agent pipeline (Analyst→Reporter→Ready)  │   └── AgentLog.jsx      # Real-time agent thought process viewer  └── pages/      ├── AnalyzePage.jsx   # File upload with SSE streaming      ├── DashboardPage.jsx # Charts, stats, forecasts, alerts      ├── HistoryPage.jsx   # Timeline of past analyses with comparison      ├── ChatPage.jsx      # Natural language query interface      └── AuditPage.jsx     # Ledger audit file upload   `

### Key UI Features

*   **StoryBoard Component:** Visualizes the agent pipeline (Stock Analyst → Business Reporter → Ready)
    
*   **AgentLog Component:** Real-time streaming of agent thoughts via SSE
    
*   **Dashboard:** Pie charts (stock health), bar charts (critical items), line charts (forecasts)
    
*   **History Comparison:** Select two runs and generate AI-powered narrative comparison
    

7\. Dependencies & How to Run
-----------------------------

### Backend Dependencies (Python)

The project uses a Python virtual environment (.venv/) with key packages:

*   **crewai**: Multi-agent orchestration framework
    
*   **flask + flask-cors**: REST API
    
*   **pandas + openpyxl**: Excel processing
    
*   **scikit-learn**: Linear regression for forecasting
    
*   **python-dotenv**: Environment variable management
    
*   **litellm**: LLM abstraction layer
    

### Frontend Dependencies

From package.json:

*   **react**, **react-dom**, **react-router-dom**
    
*   **recharts** (charting)
    
*   **axios** (HTTP client)
    
*   **lucide-react** (icons)
    
*   **react-markdown**
    
*   **vite** (dev server/bundler)
    

### Environment Variables Required (.env)

Code snippet

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   GROQ_API_KEY=      # Required for LLM  FLASK_SECRET_KEY=             # Optional  GMAIL_USER=                    # Optional for email alerts  GMAIL_APP_PASSWORD=     # Optional for email alerts   `

### Running the Project

**Backend:**

Bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   cd /Users/yash/Inventory_Agent  source .venv/bin/activate  python app.py   # Starts Flask on port 5000   `

**Frontend:**

Bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   cd /Users/yash/Inventory_Agent/frontend  npm install     # If first time  npm run dev     # Starts Vite dev server (usually port 5173)   `

**Standalone CLI (without web):**

Bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python main.py  # Runs CrewAI agents directly   `

8\. Data Flow Example
---------------------

*   **Step 1:** User uploads Stock\_Summary\_2026-04-07.xlsx via frontend
    
*   **Step 2:** Frontend sends to /upload-stream (SSE endpoint)
    
*   **Step 3:** Backend saves file to /data/, starts CrewAI crew
    
*   **Step 4:** Stock Analyst Agent uses inventory\_analysis\_tool to: Parse Excel, clean numeric columns, categorize items, generate Excel report in /reports/
    
*   **Step 5:** Business Reporter Agent receives context, writes executive summary
    
*   **Step 6:** Stream Capture sends agent thoughts to frontend via SSE
    
*   **Step 7:** Results saved to SQLite database with item-level detail
    
*   **Step 8:** Frontend Dashboard shows pie charts, tables, and the AI summary
    

9\. Documentation Summary from AgenticAIProject.txt
---------------------------------------------------

This file serves as the project proposal/technical document for academic submission:

*   **Target Users:** SMEs using Tally Prime ERP
    
*   **Problem Solved:** Data overload, manual report generation, static reporting
    
*   **Current Implementation:** Stock analysis with categorization logic
    
*   **Future Roadmap (proposed for full 20-credit project):**
    
    *   **Phase 2:** Debtor Aging Analysis, Cash Flow Prediction, GST Compliance
        
    *   **Phase 3:** "Chat with Tally" using RAG
        
    *   **Phase 4:** Anomaly Detection for unusual ledger entries
        
*   **Research Questions:** CrewAI vs Hierarchical agents, hallucination mitigation, data privacy
    

10\. Summary of Technologies Used
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
