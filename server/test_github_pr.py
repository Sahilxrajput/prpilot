from dotenv import load_dotenv

load_dotenv()

from app.services.github.client import GitHubClient

github = GitHubClient()

files = github.get_pull_request_files(
    owner="Sahilxrajput",
    repo="test-repo",
    pull_number=1,
)

print(f"Found {len(files)} files\n")

for file in files:

    print("=" * 60)

    print("File:", file["filename"])
    print("Status:", file["status"])
    print("Additions:", file["additions"])
    print("Deletions:", file["deletions"])

    print("\nPatch:")
    print(file.get("patch", "No patch available"))
