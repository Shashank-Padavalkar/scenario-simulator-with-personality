# Scenario Simulator - AI Decision Intelligence

A production-quality full-stack web application that simulates possible outcomes of a user’s decision using a Retrieval-Augmented Generation (RAG) pipeline powered by the Google Gemini API.

## Features
- **Premium UI:** Dark theme dashboard with smooth transitions and glassmorphism styling.
- **RAG Pipeline:** Utilizes ChromaDB locally to perform similarity searches over predefined knowledge bases.
- **Structured AI Output:** Gemini Pro 2.5 returns structured JSON with Best Case, Worst Case, Most Likely, Risks, and Recommendations.
- **FastAPI Backend:** Robust and fast asynchronous backend to handle requests.

## Setup Instructions

### 1. Prerequisites
- Python 3.11+
- A valid Google Gemini API Key

### 2. Installation
Navigate into the project directory and install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Copy `.env.example` to `.env` and add your Gemini API Key:
```bash
# On Windows PowerShell:
cp .env.example .env
```
Edit `.env` and set:
```
GEMINI_API_KEY=your_gemini_api_key_here
VECTOR_DB_PATH=./chroma_db
```

### 4. Initialize Knowledge Base (RAG)
Before running the application, you must initialize the local ChromaDB vector store by chunking and embedding the knowledge base files. This only needs to be run once (or whenever you add new markdown files to `knowledge/`):
```bash
python -m backend.rag.knowledge_loader
```

### 5. Run the Application
Start the FastAPI backend (which also serves the static frontend):
```bash
uvicorn backend.main:app --reload
```
Open your browser and navigate to: http://127.0.0.1:8000
