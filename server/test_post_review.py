from dotenv import load_dotenv

load_dotenv()

from app.services.github.client import GitHubClient

github = GitHubClient()

review = github.create_pull_request_review(
    owner="Sahilxrajput",
    repo="test-repo",
    pull_number=1,
    body="""
## 🤖 PrPilot AI Review

This is a test review from PrPilot.

The GitHub API integration is working correctly.
""".strip(),
)

print("Review posted successfully!")

print("Review ID:", review["id"])
print("Review URL:", review["html_url"])
