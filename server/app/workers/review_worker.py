from app.services.github.client import GitHubClient
from app.services.rag.pr_review import PRReviewer


def process_pr(payload: dict):

    repository = payload["repository"]

    owner = repository["owner"]["login"]
    repo = repository["name"]

    pull_request = payload["pull_request"]

    pull_number = pull_request["number"]

    commit_id = pull_request["head"]["sha"]

    print(f"Starting review for " f"{owner}/{repo}#{pull_number}")

    # --------------------------------
    # 1. Get changed files
    # --------------------------------

    github = GitHubClient()

    files = github.get_pull_request_files(
        owner=owner,
        repo=repo,
        pull_number=pull_number,
    )

    print(f"Found {len(files)} changed files")

    # --------------------------------
    # 2. Run RAG review
    # --------------------------------

    reviewer = PRReviewer()

    review = reviewer.review_pull_request(files=files)

    print("\n")
    print("=" * 80)
    print("AI PR REVIEW")
    print("=" * 80)
    print(review)

    # --------------------------------
    # 3. Post review to GitHub
    # --------------------------------

    github_review = github.create_pull_request_review(
        owner=owner,
        repo=repo,
        pull_number=pull_number,
        body=review,
        commit_id=commit_id,
    )

    print("\n")
    print("=" * 80)
    print("REVIEW POSTED")
    print("=" * 80)

    print("Review ID:", github_review["id"])

    print("Review URL:", github_review.get("html_url"))

    return github_review
