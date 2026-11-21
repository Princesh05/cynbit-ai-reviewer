
import os
import requests

from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

GITHUB_API_URL = "https://api.github.com"


def get_github_headers():
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    return headers


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

    if response.status_code == 404:
        raise ValueError("Repository not found or inaccessible.")

    if response.status_code == 401:
        raise ValueError("Invalid GitHub token.")

    if response.status_code == 403:
        raise ValueError(
            "GitHub API rate limit exceeded or permission denied."
        )

    response.raise_for_status()

    pull_requests = response.json()

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
