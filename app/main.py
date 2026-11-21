
from fastapi import FastAPI, HTTPException
from requests.exceptions import RequestException

from app.ai.routes import router as ai_router
from app.agents.pr_workflow import run_pr_workflow
from app.database.db import save_pr_analysis

from app.github.client import (
    get_pull_requests,
    get_pull_request_files,
    get_pull_request_details,
    get_pull_request_file_content,
)


# --------------------------------------------------
# 1. FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="Cynbit AI Pull Request Intelligence",
    description="AI-powered code review and developer mentorship system",
    version="1.0.0",
)

app.include_router(ai_router)


# --------------------------------------------------
# 2. HOME ENDPOINT
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to Cynbit AI Reviewer",
        "status": "running",
        "project": "AI Pull Request Intelligence System",
    }


# --------------------------------------------------
# 3. HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Cynbit AI Reviewer",
    }


# --------------------------------------------------
# 4. FETCH GITHUB PULL REQUESTS
# --------------------------------------------------

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
        raise HTTPException(status_code=404, detail=str(error))

    except RequestException:
        raise HTTPException(
            status_code=502,
            detail="Unable to communicate with GitHub API.",
        )


# --------------------------------------------------
# 5. FETCH PULL REQUEST CHANGED FILES
# --------------------------------------------------

@app.get("/github/{owner}/{repo}/pulls/{pull_number}/files")
def fetch_github_pull_request_files(
    owner: str,
    repo: str,
    pull_number: int,
):

    try:
        changed_files = get_pull_request_files(
            owner,
            repo,
            pull_number,
        )

        return {
            "success": True,
            "repository": f"{owner}/{repo}",
            "pull_request_number": pull_number,
            "total_changed_files": len(changed_files),
            "files": changed_files,
        }

    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

    except RequestException:
        raise HTTPException(
            status_code=502,
            detail="Unable to fetch Pull Request files from GitHub.",
        )


# --------------------------------------------------
# 6. AUTOMATIC GITHUB PULL REQUEST ANALYSIS
# --------------------------------------------------

@app.post(
    "/github/{owner}/{repo}/pulls/{pull_number}/analyze"
)
def analyze_github_pull_request(
    owner: str,
    repo: str,
    pull_number: int,
):

    try:
        # Fetch PR details and head commit
        pr_details = get_pull_request_details(
            owner,
            repo,
            pull_number,
        )

        head_sha = pr_details["head"]["sha"]

        # Fetch changed files
        changed_files = get_pull_request_files(
            owner,
            repo,
            pull_number,
        )

        if not changed_files:
            raise HTTPException(
                status_code=400,
                detail="No changed files found in this Pull Request.",
            )

        # Select Python files, excluding deleted files
        python_files = [
            file for file in changed_files
            if file["filename"].endswith(".py")
            and file["status"] != "removed"
        ]

        if not python_files:
            raise HTTPException(
                status_code=400,
                detail="This Pull Request contains no analyzable Python files.",
            )

        # Retrieve complete Python source code
        code_parts = []

        for file in python_files:

            filename = file["filename"]

            content = get_pull_request_file_content(
                owner=owner,
                repo=repo,
                filename=filename,
                ref=head_sha,
            )

            code_parts.append(
                f"\n# =====================================\n"
                f"# FILE: {filename}\n"
                f"# =====================================\n\n"
                f"{content}"
            )

        combined_code = "\n\n".join(code_parts)

        # Calculate PR statistics using GitHub metadata
        files_changed = len(changed_files)

        lines_added = sum(
            file["additions"] for file in changed_files
        )

        lines_deleted = sum(
            file["deletions"] for file in changed_files
        )

        # Run the existing LangGraph workflow
        question = (
            "Review the changed Python files from this GitHub Pull Request. "
            "Explain important issues, potential bugs, code quality problems, "
            "and practical improvements for a junior developer."
        )

        result = run_pr_workflow(
            code=combined_code,
            files_changed=files_changed,
            lines_added=lines_added,
            lines_deleted=lines_deleted,
            question=question,
        )

        # Save analysis in SQLite
        analysis_id = save_pr_analysis(
            code=combined_code,
            files_changed=files_changed,
            lines_added=lines_added,
            lines_deleted=lines_deleted,
            question=question,
            result=result,
        )

        return {
            "success": True,
            "message": "GitHub Pull Request analyzed successfully.",
            "repository": f"{owner}/{repo}",
            "pull_request_number": pull_number,
            "pull_request_title": pr_details["title"],
            "head_commit": head_sha,
            "analysis_id": analysis_id,
            "total_changed_files": files_changed,
            "python_files_analyzed": [
                file["filename"] for file in python_files
            ],
            "lines_added": lines_added,
            "lines_deleted": lines_deleted,
            "analysis": result,
        }

    except HTTPException:
        raise

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except RequestException:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve Pull Request data from GitHub.",
        )
