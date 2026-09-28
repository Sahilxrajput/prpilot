from dotenv import load_dotenv

load_dotenv()

from app.services.github.client import GitHubClient
from app.services.rag.pr_review import PRReviewer

github = GitHubClient()

files = github.get_pull_request_files(
    owner="Sahilxrajput",
    repo="test-repo",
    pull_number=1,
)

reviewer = PRReviewer()

review = reviewer.review_pull_request(files=files)

print("\n")
print("=" * 80)
print("PR REVIEW")
print("=" * 80)
print()
print(review)
