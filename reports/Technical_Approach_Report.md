
# Technical Approach Report
## Cynbit AI – Pull Request Intelligence & Developer Mentorship

### 1. Purpose and Scope

This document describes the technical approach used in the existing Cynbit AI proof of concept.

The application assists human Pull Request review by combining GitHub integration, static Python analysis, experimental risk prediction, AI-powered code review, and developer mentorship.

It does not automatically approve, merge, close, or modify GitHub pull requests.

### 2. System Architecture

The prototype contains the following components:

| Component | Responsibility |
|---|---|
| Streamlit Dashboard | User interface for repository and PR analysis |
| FastAPI Backend | API endpoints and analysis orchestration |
| GitHub Client | Retrieves PR details, changed files, and Python source |
| Static Analyzer | Performs basic Python source checks |
| Risk Prediction | Produces an experimental PR risk estimate |
| Gemini and Groq | AI review and mentorship generation |
| ChromaDB / RAG | Retrieves relevant programming knowledge |
| LangGraph | Coordinates PR analysis workflow |
| SQLite | Stores analysis history |

### 3. End-to-End Data Pipeline

The automatic GitHub PR analysis workflow follows these steps:

1. The user provides a GitHub repository and PR number.
2. The backend retrieves PR details, including the head commit SHA.
3. The GitHub client retrieves the changed-file list.
4. Python files are selected; removed files are excluded.
5. Source code is retrieved at the PR head commit.
6. The source code is passed into the PR analysis workflow.
7. Static analysis and the configured risk-assessment step are executed.
8. AI review and mentorship stages generate feedback, with RAG retrieval supporting mentorship.
9. The analysis is saved in SQLite.
10. Results are returned through the API and displayed in Streamlit.

The automatic GitHub analysis path currently focuses on Python files.

### 4. Model and Technology Choices

#### 4.1 Static Python Analysis

A lightweight static-analysis step checks Python source for basic issues.

It provides deterministic information that complements AI-generated feedback.

It is not a replacement for comprehensive linting, type checking, security scanning, or automated testing.

#### 4.2 PR Risk Prediction

The project includes an experimental Random Forest-based risk prediction component.

**Limitation:** The current model uses only 15 synthetic examples and has not been validated against real historical PR outcomes.

Its output should be treated as an exploratory estimate, not a production-ready risk score.

A reliable model would require representative historical PR data, clearly defined risk labels, separate training and testing datasets, and evaluation using appropriate metrics.

#### 4.3 LLM-Assisted Review and Mentorship

The prototype integrates Gemini and Groq for AI review and mentorship tasks, according to the configured workflow.

The language models generate natural-language explanations and suggestions.

Their outputs may be incomplete or incorrect and should always be verified by a developer.

#### 4.4 Retrieval-Augmented Generation (RAG)

ChromaDB supports the mentorship knowledge retrieval process.

Relevant programming knowledge is retrieved and supplied as context for developer mentorship responses.

The quality of retrieval depends on the relevance and freshness of the indexed knowledge.

#### 4.5 LangGraph

LangGraph coordinates the PR workflow stages.

It provides a structured way to organize analysis steps and a foundation for adding validation and human-review checkpoints.

### 5. Prompt Engineering and Output Design

The LLM stages should receive task-specific instructions and structured context.

For AI code review, useful context includes:

- Repository and PR metadata.
- Changed Python file names.
- Relevant source-code content.
- Static-analysis findings, where available.
- Instructions to distinguish observed facts from assumptions.

For developer mentorship, useful context includes:

- Relevant code or findings.
- Retrieved learning material.
- The specific concept requiring explanation.
- A request for actionable, beginner-friendly suggestions.

Recommended output fields for future standardization include:

- `summary`
- `findings`
- `severity`
- `evidence`
- `suggestion`
- `confidence_or_uncertainty`

Prompts should instruct models not to invent code behavior, test results, or repository facts.

These are recommended prompt-design practices; the exact prompt text should be checked against the current source code before claiming every instruction is already implemented.

### 6. API and User Interface

The existing backend exposes these routes:

| Endpoint | Purpose |
|---|---|
| `GET /` | Root/status response |
| `GET /health` | Health check |
| `GET /github/{owner}/{repo}/pulls` | Retrieve repository pull requests |
| `POST /github/{owner}/{repo}/pulls/{pull_number}/analyze` | Automatic GitHub PR analysis |
| `POST /ai/review` | AI review workflow |
| `POST /ai/mentor` | Developer mentorship workflow |
| `POST /ai/pr-workflow` | PR workflow endpoint |

The Streamlit dashboard supports GitHub PR retrieval, analysis, results display, manual workflow use, and analysis history.

### 7. Data Storage and Security

SQLite is used for local persistence of analysis history.

GitHub API access can use an optional GitHub token through environment configuration.

Before production use:

- Keep API keys and tokens out of source control.
- Use least-privilege GitHub permissions.
- Avoid logging secrets or unnecessary source code.
- Define data retention and deletion policies.
- Add authentication and authorization.
- Review external LLM provider data-processing terms.
- Consider removing secrets and sensitive information before sending code to an external model.
- Add audit logging and rate limiting.

The current prototype should not be described as production-secure or production-deployed.

### 8. Evaluation Plan

A suitable evaluation plan would include:

| Area | Evaluation method |
|---|---|
| Static Analysis | Compare findings with manually reviewed examples |
| AI Review | Human reviewers assess correctness and usefulness |
| Risk Prediction | Evaluate on labelled PRs using precision, recall, F1-score, and confusion matrix |
| Mentorship | Collect developer feedback on clarity and usefulness |
| Reliability | Test API errors, GitHub rate limits, and provider failures |
| Performance | Measure analysis time across different PR sizes |

The successful prototype test demonstrates that the integration path can run. It does not establish model accuracy or business impact.

### 9. Implementation Status and Limitations

**Implemented in the prototype:**

- FastAPI backend and Streamlit dashboard.
- GitHub PR metadata and changed-file retrieval.
- Python source retrieval at the PR head commit.
- Automatic PR analysis endpoint.
- Static analysis and experimental risk assessment.
- Gemini/Groq integrations for review and mentorship.
- ChromaDB-based RAG mentorship support.
- LangGraph workflow orchestration.
- SQLite analysis history.

**Known limitations:**

- Automatic source analysis focuses on Python files.
- The risk model uses a small synthetic dataset and is not validated on real PR outcomes.
- Static analysis is basic.
- LLM output quality and availability depend on external providers, network access, and quota.
- The prototype has not been established as a production deployment.
- Evaluation on a representative labelled dataset remains future work.

### 10. Proposed Execution Plan

| Phase | Work |
|---|---|
| 1. Baseline Validation | Test the workflow on representative PRs |
| 2. Evaluation Dataset | Collect approved historical examples and define risk labels |
| 3. Quality Improvements | Add tests, structured output validation, and stronger error handling |
| 4. Human Feedback | Capture reviewer and developer feedback |
| 5. Security Review | Improve access control, secret handling, and data retention |
| 6. Pilot Assessment | Compare measured outcomes against the existing review process |

### 11. Conclusion

Cynbit AI combines GitHub integration, static Python analysis, experimental risk estimation, LLM-assisted review, RAG-based mentorship, and workflow orchestration in a working prototype.

The recommended next step is a controlled evaluation using approved PR examples and human reviewers.

Production adoption should depend on demonstrated quality, security, reliability, and measurable value.
