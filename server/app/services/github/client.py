import os

import httpx


class GitHubClient:

    BASE_URL = "https://api.github.com"

    def __init__(self):

        self.token = os.getenv("GITHUB_TOKEN")

        if not self.token:
            raise RuntimeError("GITHUB_TOKEN is missing")

        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": "2026-03-10",
        }

    def get_pull_request_files(
        self,
        owner: str,
        repo: str,
        pull_number: int,
    ) -> list[dict]:

        url = f"{self.BASE_URL}/repos/" f"{owner}/{repo}/pulls/{pull_number}/files"

        response = httpx.get(
            url,
            headers=self.headers,
            params={"per_page": 100},
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def create_pull_request_review(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        body: str,
        commit_id: str | None = None,
    ) -> dict:

        url = (
            f"{self.BASE_URL}/repos/" f"{owner}/{repo}/pulls/" f"{pull_number}/reviews"
        )

        payload = {
            "body": body,
            "event": "COMMENT",
        }

        if commit_id:
            payload["commit_id"] = commit_id

        response = httpx.post(
            url,
            headers=self.headers,
            json=payload,
            timeout=30,
        )

        if response.status_code >= 400:
            print("GitHub API error:")
            print("Status:", response.status_code)
            print("Response:", response.text)

        response.raise_for_status()

        return response.json()
