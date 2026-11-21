
from fastapi import FastAPI, HTTPException
from requests.exceptions import RequestException
from app.ai.routes import router as ai_router

from app.github.client import get_pull_requests

app = FastAPI(
    title="Cynbit AI Pull Request Intelligence",
    description="AI-powered code review and developer mentorship system",
    version="1.0.0",
)
# Register AI Code Reviewer routes
app.include_router(ai_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to Cynbit AI Reviewer",
        "status": "running",
        "project": "AI Pull Request Intelligence System",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Cynbit AI Reviewer",
    }


@app.get("/github/{owner}/{repo}/pulls")
def fetch_github_pull_requests(owner: str, repo: str):
    try:
        pull_requests = get_pull_requests(owner, repo)

        return {
            "success": True,
            "repository": f"{owner}/{repo}",
            "total_pull_requests": len(pull_requests),
            "pull_requests": pull_requests,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except RequestException:
        raise HTTPException(
            status_code=502,
            detail="Unable to communicate with GitHub API.",
        )
