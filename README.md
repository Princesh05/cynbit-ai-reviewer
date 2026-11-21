
# 🤖 Cynbit AI – Pull Request Intelligence & Developer Mentorship

An AI-powered Pull Request intelligence platform that analyzes Python code, detects potential issues, predicts Pull Request risk, integrates with GitHub repositories, and provides intelligent developer mentorship.

## 🚀 Project Overview

Cynbit AI is an intelligent code review and developer mentorship platform designed to help developers improve code quality and identify potential problems before merging Pull Requests.

The platform combines Static Code Analysis, Machine Learning, Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), GitHub REST API integration, and LangGraph to generate comprehensive Pull Request analysis reports.

## ✨ Key Features

- **Static Code Analysis:** Detects Python syntax errors and basic code quality issues, including unused imports, unused variables, and long lines.
- **ML-Based PR Risk Prediction:** Predicts Low, Medium, or High risk based on Pull Request statistics and detected issues.
- **AI Code Review:** Uses Google Gemini with Groq fallback to identify potential logical errors, code quality concerns, and improvement opportunities.
- **Developer Mentorship:** Uses RAG to retrieve relevant Python programming knowledge and generate learning-oriented explanations.
- **GitHub Integration:** Connects with public GitHub repositories through the GitHub REST API and fetches repository Pull Requests.
- **Automatic PR Analysis:** Retrieves Pull Request details, identifies changed Python files, fetches source code at the PR head commit, and sends it through the complete analysis workflow.
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
│   │   ├── Fetch Pull Requests
│   │   ├── Fetch PR Details
│   │   └── Retrieve Changed Python Files
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

Configure your AI provider credentials:

```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
GITHUB_TOKEN=
```

**Important:**

- Keep all API keys private.
- Never upload your `.env` file to GitHub.
- A GitHub token is optional for accessing public repositories.
- Authenticated requests can provide higher API rate limits and private repository access, subject to token permissions.
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
| GET | `/github/{owner}/{repo}/pulls` | Fetch repository Pull Requests |
| POST | `/github/{owner}/{repo}/pulls/{pull_number}/analyze` | Automatically analyze a GitHub Pull Request |
| POST | `/ai/review` | AI-powered Python code review |
| POST | `/ai/mentor` | RAG-based developer mentorship |
| POST | `/ai/pr-workflow` | Execute the complete PR analysis workflow |

## 🧠 How the PR Analysis Workflow Works

The LangGraph workflow coordinates the following stages:

1. **GitHub Integration:** Retrieves Pull Request details and changed files from the selected repository.
2. **Source Code Retrieval:** Fetches eligible Python source files from the Pull Request head commit.
3. **Static Analysis:** Checks submitted Python code for syntax errors and basic code quality issues.
4. **Risk Prediction:** Uses a Random Forest model to predict Pull Request risk.
5. **AI Code Review:** Generates code review feedback using Google Gemini or Groq fallback.
6. **Developer Mentorship:** Retrieves relevant programming knowledge from ChromaDB and generates educational explanations.
7. **Final Report:** Combines the analysis results into a structured response and stores the analysis in SQLite.

## 📊 Example Analysis

**Input Python Code:**

```python
def calculate_total(price, quantity):
    discount = 10
    total = price * quantity
    return total
```

The current static analyzer can identify the unused `discount` variable and report relevant code quality issues.

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

- **GitHub Integration:** Public repository lookup and Pull Request fetching are implemented and tested through the FastAPI backend and Streamlit dashboard.
- **Automatic PR Code Analysis:** Retrieves Pull Request details, identifies changed Python files, fetches their source code at the PR head commit, and executes the analysis workflow. This functionality has been successfully tested with a GitHub Pull Request.
- **Experimental ML Model:** The risk predictor uses a small synthetic dataset of 15 examples. Its predictions have not been validated against real-world Pull Request outcomes.
- **Static Analysis:** Implements basic Python checks and is not a complete security scanner or replacement for professional linting tools.
- **AI Availability:** AI responses depend on external model availability, API quotas, and network connectivity.
- **Analysis Scope:** Automatic GitHub analysis currently focuses on eligible Python files. It does not provide a complete multi-language or line-level review system.
- **MVP Status:** The application is a working prototype and has not been validated for production use.

## 🔮 Future Improvements

- Analyze individual changed files and provide line-level review feedback.
- Support multiple programming languages.
- Train the risk prediction model using real historical Pull Request data.
- Improve security and vulnerability detection.
- Add authentication and role-based access control.
- Introduce advanced team-level analytics and reporting.
- Explore deployment, monitoring, and production scalability.
- Improve automated testing and model evaluation.

## 📸 Screenshots

Add screenshots of the following application features to a `screenshots/` folder in the repository:

1. Main dashboard and project metrics.
2. GitHub repository integration and Pull Request list.
3. Successful automatic Pull Request analysis.
4. AI code review and developer mentorship.
5. Pull Request analytics and analysis history.

Example:

```text
screenshots/
├── dashboard.png
├── github-integration.png
├── pr-analysis.png
├── ai-review.png
└── analytics.png
```

After adding the images, you can embed them here:

```markdown
![Cynbit AI Dashboard](screenshots/dashboard.png)
![GitHub Integration](screenshots/github-integration.png)
![PR Analysis](screenshots/pr-analysis.png)
```

## 👨‍💻 Author

**Prince Kumar Sharma**

B.Tech – Computer Science & Engineering (AI & ML)

- **GitHub:** https://github.com/Princesh05
- **LinkedIn:** https://www.linkedin.com/in/prince-kumar-sharma-415927314/

---

**Cynbit AI – Making Code Reviews Smarter and Developer Learning Better.**
