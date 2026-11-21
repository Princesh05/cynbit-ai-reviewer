# 🤖 Cynbit AI – Pull Request Intelligence & Developer Mentorship

An AI-powered Pull Request intelligence platform that analyzes Python code, detects potential issues, predicts PR risk, integrates with GitHub repositories, and provides intelligent developer mentorship.

## 🚀 Project Overview

Cynbit AI is an intelligent code review and developer mentorship platform designed to help developers improve code quality and identify potential problems before merging Pull Requests.

The platform combines Static Code Analysis, Machine Learning, Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), GitHub REST API integration, and LangGraph to generate comprehensive Pull Request analysis reports.

## ✨ Key Features

- **Static Code Analysis:** Detects Python syntax errors, unused imports, unused variables, and long lines.
- **ML-Based PR Risk Prediction:** Predicts Low, Medium, or High risk based on Pull Request statistics and detected issues.
- **AI Code Review:** Uses Google Gemini with Groq fallback to identify potential logical errors, code quality concerns, and improvement opportunities.
- **Developer Mentorship:** Uses RAG to retrieve relevant Python programming knowledge and generate learning-oriented explanations.
- **GitHub Integration:** Connects with public GitHub repositories through the GitHub REST API and fetches repository Pull Requests.
- **LangGraph Workflow:** Coordinates static analysis, risk prediction, AI code review, and developer mentorship in a unified workflow.
- **Interactive Dashboard:** Provides PR analysis results, risk distribution, issue statistics, GitHub integration, and persistent analysis history.
- **Persistent Storage:** Stores Pull Request analysis records using SQLite.
- **REST API:** Provides backend endpoints through FastAPI with interactive Swagger documentation.

## 🏗️ Project Architecture

```text
Cynbit AI Reviewer
│
├── Streamlit Dashboard
│
├── FastAPI Backend
│   │
│   ├── GitHub API Client
│   │
│   ├── Static Code Analyzer
│   │
│   ├── ML Risk Predictor
│   │
│   ├── AI Code Reviewer
│   │   ├── Google Gemini
│   │   └── Groq Fallback
│   │
│   ├── RAG Developer Mentor
│   │   ├── LangChain
│   │   ├── Sentence Transformers
│   │   └── ChromaDB
│   │
│   └── LangGraph PR Workflow
│
├── SQLite Database
│
└── Local Vector Database
```

## 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| Machine Learning | Scikit-learn, Random Forest |
| Generative AI | Google Gemini, Groq |
| RAG Framework | LangChain |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers |
| Agent Workflow | LangGraph |
| GitHub Integration | GitHub REST API, Requests |
| Database | SQLite |
| Testing | Pytest |
| API Documentation | Swagger UI |

## 📁 Project Structure

```text
cynbit-ai-reviewer/
│
├── app/
│   ├── analyzer/
│   │   └── code_analyzer.py
│   │
│   ├── ai/
│   │   ├── llm_client.py
│   │   ├── code_reviewer.py
│   │   ├── developer_mentor.py
│   │   ├── knowledge_base.py
│   │   ├── vector_store.py
│   │   └── routes.py
│   │
│   ├── agents/
│   │   └── pr_workflow.py
│   │
│   ├── database/
│   │   └── db.py
│   │
│   ├── github/
│   │   └── client.py
│   │
│   ├── ml/
│   │   └── risk_predictor.py
│   │
│   └── main.py
│
├── dashboard/
│   └── dashboard.py
│
├── data/
│
├── tests/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Princesh05/cynbit-ai-reviewer.git
cd cynbit-ai-reviewer
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

**Windows Command Prompt:**

```cmd
.venv\Scripts\activate.bat
```

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root directory using `.env.example` as a reference.

Configure the required AI provider credentials:

```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
GITHUB_TOKEN=
```

**Important:**
- Keep all API keys private.
- Never upload your `.env` file to GitHub.
- A GitHub token is optional for accessing public repositories. Authenticated requests can be configured for higher API rate limits and private repository access, subject to token permissions.
- Use read-only repository permissions when configuring GitHub access.

### 6. Start the FastAPI Backend

Open a terminal from the project root directory:

```bash
python -m uvicorn app.main:app --reload
```

Backend URL:

http://127.0.0.1:8000

Swagger API Documentation:

http://127.0.0.1:8000/docs

### 7. Start the Streamlit Dashboard

Open a second terminal from the project root directory and activate the same virtual environment.

Run:

```bash
python -m streamlit run dashboard/dashboard.py
```

Dashboard URL:

http://localhost:8501

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome endpoint |
| GET | `/health` | Backend health check |
| GET | `/github/{owner}/{repo}/pulls` | Fetch repository Pull Requests from GitHub |
| POST | `/ai/review` | AI-powered Python code review |
| POST | `/ai/mentor` | RAG-based developer mentorship |
| POST | `/ai/pr-workflow` | Execute the complete PR analysis workflow |

## 🧠 How the PR Analysis Workflow Works

The LangGraph workflow coordinates the following stages:

1. **Static Analysis:** Checks submitted Python code for syntax errors and basic code quality issues.
2. **Risk Prediction:** Uses a Random Forest model to predict Pull Request risk.
3. **AI Code Review:** Generates code review feedback using Google Gemini or Groq fallback.
4. **Developer Mentorship:** Retrieves relevant programming knowledge from ChromaDB and generates educational explanations.
5. **Final Report:** Combines the analysis results into a structured response.

## 📊 Example Analysis

**Input Python Code:**

```python
def calculate_total(price, quantity):
    discount = 10
    total = price * quantity
    return total
```

The current static analyzer can identify the unused `discount` variable and provide information about detected code quality issues.

**Generated Analysis Includes:**

- Python syntax validation.
- Static code analysis results.
- Predicted Pull Request risk.
- AI-generated code review.
- RAG-based developer mentorship.
- Suggested code improvements.
- Combined analysis report.

## 🧪 Testing

Run the automated test suite:

```bash
python -m pytest tests/ -v
```

The test suite covers implemented static analysis, risk prediction, vector store functionality, and other tested project components.

## ⚠️ Current Implementation Status and Limitations

- **GitHub Integration:** Public repository lookup and Pull Request fetching have been implemented and tested through the FastAPI backend and Streamlit dashboard.
- **Automatic PR Code Analysis:** Fetching actual GitHub Pull Request changed files and diffs and sending them through the complete analysis workflow is still under development.
- **Experimental ML Model:** The risk predictor is trained on a small synthetic dataset of 15 examples. Its predictions have not been validated against real-world Pull Request outcomes.
- **Static Analysis:** Implements basic Python checks and is not a complete security scanner or replacement for professional linting tools.
- **AI Availability:** AI responses depend on external model availability, API quotas, and network connectivity.
- **MVP Status:** The application is a prototype and has not been validated for production use.

## 🔮 Future Improvements

- Complete end-to-end GitHub Pull Request code analysis.
- Automatically retrieve changed files and code diffs from GitHub PRs.
- Analyze individual changed files and provide line-level review feedback.
- Support multiple programming languages.
- Train the risk prediction model using real historical Pull Request data.
- Improve security and vulnerability detection.
- Add authentication and role-based access control.
- Introduce advanced team-level analytics and reporting.
- Explore deployment, monitoring, and production scalability.

## 👨‍💻 Author

**Prince Kumar Sharma**

B.Tech – Computer Science & Engineering (AI & ML)

- **GitHub:** https://github.com/Princesh05
- **LinkedIn:** https://www.linkedin.com/in/prince-kumar-sharma-415927314/

---

**Cynbit AI – Making Code Reviews Smarter and Developer Learning Better.**
