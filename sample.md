<div align="center">

# 🧠 InsightScope
### Intelligent Enterprise Knowledge Assistant

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square)](https://python.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6B6B?style=flat-square)](https://www.trychroma.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white)](https://openai.com/)

Turning organizational data chaos into cognitive clarity — powered by LLMs and vector search.

[Overview](#overview) • [Features](#features) • [Getting Started](#getting-started) • [Deployment](#deployment) • [Project Structure](#project-structure)

</div>

## Overview

**InsightScope** is a Retrieval-Augmented Generation (RAG) based AI assistant that enables teams to query internal company documents, reports, and emails using natural language. It delivers accurate, context-aware responses backed by real data, complete with exact source citations. Think of it as ChatGPT, but specifically grounded in your organization's internal knowledge base.

## Features

- **Natural Language Queries**: Ask complex questions about your data in plain English.
- **Smart Retrieval**: Retrieves the most relevant context using ChromaDB/FAISS vector search.
- **Context-Aware Responses**: Grounded answers generated strictly from your uploaded files.
- **Source Citations**: View the exact document snippets and confidence scores used for each answer.
- **Prompt Engineering Playground**: Built-in personas (Standard, Formal Corporate, Analyst Summary, Concise Bullets) to adapt the response tone.
- **Multi-Format Ingestion**: Process PDFs, text files, and DOCX files automatically.
- **Local & Privacy-First**: Run entirely on your local machine using models like GPT4All/Ollama to maintain complete data privacy.

## System Architecture

```text
           ┌─────────────────────┐ 
           │    Streamlit UI     │ 
           └─────────┬───────────┘ 
                     │ Query 
                     ▼ 
           ┌─────────────────────┐ 
           │ LangChain/Pipeline  │ 
           └─────────┬───────────┘ 
                     │ 
          ┌──────────┴───────────┐ 
          │    ChromaDB/FAISS    │ ← Indexed embeddings 
          └──────────┬───────────┘ 
                     │ 
          ┌──────────┴───────────┐ 
          │  LLM (OpenAI/Local)  │ ← Context-augmented generation
          └──────────┬───────────┘ 
                     │ 
                     ▼ 
           ┌─────────────────────┐ 
           │  Formatted Response │ 
           └─────────────────────┘ 
```

## Getting Started

> [!NOTE]
> InsightScope requires Python 3.8 or higher. If you prefer using OpenAI models over local alternatives, you'll need an active OpenAI API key.

### 1. Prerequisites

- Python 3.8+
- MongoDB (running locally or remotely)
- Git

### 2. Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/insight_scope.git
cd insight_scope

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Configure your environment settings:

> [!TIP]
> InsightScope supports multiple LLM providers: **GPT4All** (runs locally, no API key), **Ollama** (runs locally), and **OpenAI** (requires API key).

```bash
# Create your configuration file
cp .env.example .env
```

Ensure your `.env` is tailored to your chosen `LLM_PROVIDER`. For OpenAI, add your `OPENAI_API_KEY`.

### 4. Running Locally

Start the application using the built-in runner script:

```bash
# Launch the Streamlit frontend
python run.py run
```

The application will be available at `http://localhost:8501`. 

> [!TIP]
> You can drag and drop documents directly into the web UI, or process directories of documents ahead of time using:
> ```bash
> python run.py process --dir /path/to/your/custom/data
> ```

## Deployment

### Docker Deployment

The fastest way to deploy InsightScope safely in an isolated environment is using Docker and our deployment script.

> [!IMPORTANT]
> Ensure Docker and Docker Compose are installed on your target machine.

```bash
# Make the script executable
chmod +x deploy.sh

# Run the deployment orchestration script
./deploy.sh
```

### Manual Orchestration

If you prefer to start services independently:

1. Copy `.env.production` to `.env` and adjust the variables.
2. Spin up the containers:
   ```bash
   docker-compose up -d
   ```
3. Validate the live deployment:
   ```bash
   python validate_deployment.py
   ```

For more comprehensive setup details regarding production servers, review the included `DEPLOYMENT.md` guide.

## Project Structure

Understanding the layout of the repository will help you navigate the codebase for customizations.

```text
insight_scope/
├── app/                     # Core application layers
│   ├── api/                 # Backend pipelines (e.g., data_ingestion.py)
│   └── frontend/            # Custom Streamlit UI components (app.py)
├── config/                  # Configuration settings and env validation
├── data/                    
│   ├── processed/           # Sanitized data ready for chunking
│   └── raw/                 # Original ingested documents (PDF, TXT, DOCX)
├── models/                  # Core RAG intelligence
│   ├── embeddings/          # Embedding generation & VectorStore logic
│   └── llm/                 # Generative AI execution routines
├── utils/                   # Shared utilities
│   ├── evaluation/          # Tooling to benchmark query relevance
│   ├── preprocessing/       # Doc loaders and custom chunkers
│   └── mongodb_connector.py # Database interactions for logging metrics
├── vector_db/               # Persistent database storage for FAISS/Chroma
├── deploy.sh                # End-to-end Docker deployment script
├── docker-compose.yml       # Dev/production multi-container definitions
├── requirements.txt         # Python package dependencies
├── run.py                   # Main CLI entry point for processing/hosting
└── validate_deployment.py   # Health check script for Docker services
```

## Configuration Reference

The `.env` file controls how the application behaves. Here are the core variables you can configure:

- **`LLM_PROVIDER`**: Choose your engine (`openai`, `ollama`, or `gpt4all`).
- **`OPENAI_API_KEY`**: Your secret key (required *only* if using OpenAI).
- **`OLLAMA_MODEL`** / **`OLLAMA_BASE_URL`**: Network settings for your local Ollama instance (defaults to `http://localhost:11434` / `llama3`).
- **`VECTOR_DB_TYPE`**: Switch between `chroma` (default) and `faiss` storage structures.
- **`EMBEDDING_MODEL`**: The HuggingFace sentence transformer used for generic embeddings (default: `sentence-transformers/all-MiniLM-L6-v2`).
- **`MONGODB_URI`**: Connection string applied when logging system metrics/telemetry.

