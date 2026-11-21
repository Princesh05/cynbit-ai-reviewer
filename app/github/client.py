
import os
import base64
import requests

from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_URL = "https://api.github.com"


# --------------------------------------------------
# 1. GITHUB HEADERS
# --------------------------------------------------

def get_github_headers():

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    return headers


# --------------------------------------------------
# 2. HANDLE GITHUB API RESPONSES
# --------------------------------------------------

def handle_github_response(response):

    if response.status_code == 404:
        raise ValueError(
            "Repository or Pull Request not found or inaccessible."
        )

    if response.status_code == 401:
        raise ValueError("Invalid GitHub token.")

    if response.status_code == 403:
        raise ValueError(
            "GitHub API rate limit exceeded or permission denied."
        )

    response.raise_for_status()

    return response.json()


# --------------------------------------------------
# 3. FETCH REPOSITORY PULL REQUESTS
# --------------------------------------------------

def get_pull_requests(owner: str, repo: str):

    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls"

    params = {
        "state": "open",
        "per_page": 10,
    }

    response = requests.get(
        url,
        headers=get_github_headers(),
        params=params,
        timeout=20,
    )

    pull_requests = handle_github_response(response)

    results = []

    for pr in pull_requests:

        results.append({
            "number": pr["number"],
            "title": pr["title"],
            "state": pr["state"],
            "author": pr["user"]["login"],
            "url": pr["html_url"],
            "created_at": pr["created_at"],
            "updated_at": pr["updated_at"],
        })

    return results


# --------------------------------------------------
# 4. FETCH PULL REQUEST CHANGED FILES AND DIFFS
# --------------------------------------------------

def get_pull_request_files(
    owner: str,
    repo: str,
    pull_number: int
):

    url = (
        f"{GITHUB_API_URL}/repos/{owner}/{repo}"
        f"/pulls/{pull_number}/files"
    )

    results = []
    page = 1

    while True:

        params = {
            "per_page": 100,
            "page": page,
        }

        response = requests.get(
            url,
            headers=get_github_headers(),
            params=params,
            timeout=30,
        )

        files = handle_github_response(response)

        if not files:
            break

        for file in files:

            results.append({
                "filename": file.get("filename", "Unknown"),
                "status": file.get("status", "Unknown"),
                "additions": file.get("additions", 0),
                "deletions": file.get("deletions", 0),
                "changes": file.get("changes", 0),
                "patch": file.get("patch", None),
            })

        if len(files) < 100:
            break

        page += 1

    return results


# --------------------------------------------------
# 5. FETCH COMPLETE PULL REQUEST DETAILS
# --------------------------------------------------

def get_pull_request_details(
    owner: str,
    repo: str,
    pull_number: int
):

    url = (
        f"{GITHUB_API_URL}/repos/{owner}/{repo}"
        f"/pulls/{pull_number}"
    )

    response = requests.get(
        url,
        headers=get_github_headers(),
        timeout=30,
    )

    return handle_github_response(response)


# --------------------------------------------------
# 6. FETCH COMPLETE FILE CONTENT FROM GITHUB
# --------------------------------------------------

def get_pull_request_file_content(
    owner: str,
    repo: str,
    filename: str,
    ref: str
):
    """Fetch complete file content from a specific GitHub commit."""

    url = (
        f"{GITHUB_API_URL}/repos/{owner}/{repo}"
        f"/contents/{filename}"
    )

    params = {
        "ref": ref
    }

    response = requests.get(
        url,
        headers=get_github_headers(),
        params=params,
        timeout=30,
    )

    data = handle_github_response(response)

    if data.get("encoding") != "base64":
        raise ValueError(
            f"Unsupported file encoding: {filename}"
        )

    content = base64.b64decode(
        data["content"]
    ).decode("utf-8", errors="replace")

    return content
