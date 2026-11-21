# 🤖 Cynbit AI – Pull Request Intelligence & Developer Mentorship

An AI-powered Pull Request analysis platform that reviews Python code, detects potential issues, predicts PR risk, integrates with GitHub repositories, and provides intelligent developer mentorship.

## 🚀 Project Overview

Cynbit AI is an intelligent code review and developer mentorship platform designed to help development teams improve code quality and identify potential problems before merging Pull Requests.

The platform combines Static Code Analysis, Machine Learning, Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), GitHub API integration, and LangGraph to generate comprehensive Pull Request analysis reports.

## ✨ Key Features

- **Static Code Analysis:** Detects Python syntax errors, unused imports, unused variables, and long lines.
- **ML-Based PR Risk Prediction:** Predicts Low, Medium, or High risk based on Pull Request statistics and detected issues.
- **AI Code Review:** Uses Google Gemini with Groq fallback to identify logical errors, potential security concerns, and code quality improvements.
- **Developer Mentorship:** Uses RAG to retrieve relevant Python programming knowledge and generate learning-oriented explanations.
- **GitHub Integration:** Connects with GitHub repositories through the GitHub REST API to fetch repository Pull Requests.
- **LangGraph Workflow:** Coordinates static analysis, risk prediction, AI code review, and developer mentorship in a unified workflow.
- **Company Dashboard:** Provides PR analysis results, risk distribution, issue statistics, and persistent analysis history.
- **Persistent Storage:** Stores Pull Request analysis reports using SQLite.
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
│   └── chroma_db/
│
├── tests/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
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

Create a `.env` file in the project root directory.

```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
GITHUB_TOKEN=your_github_token
```

**Important:** Keep your API keys private. Never upload your `.env` file to GitHub.

The GitHub token is used for authenticated GitHub API requests. Use an appropriately scoped token.

### 6. Start the FastAPI Backend

```bash
uvicorn app.main:app --reload
```

Backend URL:

http://127.0.0.1:8000

Swagger API Documentation:

http://127.0.0.1:8000/docs

### 7. Start the Streamlit Dashboard

Open a second terminal from the project root and activate the same virtual environment.

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

1. **Static Analysis:** Checks submitted Python code for syntax errors and basic quality issues.
2. **Risk Prediction:** Uses a Random Forest model to predict Pull Request risk.
3. **AI Code Review:** Generates detailed code review feedback using Gemini or Groq.
4. **Developer Mentorship:** Retrieves relevant programming knowledge from ChromaDB and generates educational explanations.
5. **Final Report:** Combines all analysis results into one structured response.

## 🧪 Testing

Run the automated test suite:

```bash
python -m pytest tests/ -v
```

The test suite covers implemented static analysis, risk prediction, AI-related functionality, and other project components where tests are available.

## 📊 Example Analysis

**Input Python Code:**

```python
def calculate_total(price, quantity):
    discount = 10
    total = price * quantity
    return total
```

The system can identify the unused `discount` variable and generate suggestions to improve the function.

**Generated Analysis Includes:**

- Python syntax validation.
- Static code analysis results.
- Predicted Pull Request risk.
- AI-generated code review.
- RAG-based developer mentorship.
- Suggested corrected code.
- Combined analysis report.

## ⚠️ Current Limitations

- The ML risk predictor is trained on a small synthetic dataset of 15 examples. Its predictions are experimental and have not been validated against real historical Pull Request outcomes.
- Static analysis implements basic Python checks and is not a complete security scanner or replacement for professional linting tools.
- AI responses depend on external model availability, API quotas, and network connectivity.
- GitHub API integration is implemented for fetching repository Pull Requests, but live GitHub integration testing and validation remain pending.
- The current analysis workflow accepts submitted Python source code and Pull Request statistics; automatic analysis of fetched GitHub Pull Request diffs is not yet fully integrated.
- The application is an MVP prototype and has not been validated for production use.

## 🔮 Future Improvements

- Complete and validate end-to-end GitHub Pull Request analysis.
- Automatically retrieve and analyze changed files and code diffs from GitHub PRs.
- Support multiple programming languages.
- Train the risk prediction model using real historical Pull Request data.
- Improve security and vulnerability detection.
- Add authentication and role-based access control.
- Introduce advanced team-level analytics and reporting.
- Explore cloud deployment, monitoring, and production scalability.

## 👨‍💻 Author

**Prince Kumar Sharma**

B.Tech – Computer Science & Engineering (AI & ML)

**GitHub:** https://github.com/Princesh05

**LinkedIn:** https://www.linkedin.com/in/prince-kumar-sharma-415927314/

---

**Cynbit AI – Making Code Reviews Smarter and Developer Learning Better.**