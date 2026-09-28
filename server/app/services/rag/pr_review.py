from app.services.rag.chain import RAGChain


class PRReviewer:

    def __init__(self):
        self.rag_chain = RAGChain()

    def review_pull_request(
        self,
        files: list[dict],
    ) -> str:

        if not files:
            return "No changed files found."

        results = []

        for file in files:

            filename = file.get("filename")
            status = file.get("status")
            patch = file.get("patch")

            # Binary files or files where GitHub does not provide
            # a textual patch.
            if not patch:
                continue

            query = f"""
Review the following pull request change in {filename}.

File status:
{status}

Focus on genuine bugs, security issues, correctness problems,
and reliability issues introduced by this change.

Do not report style preferences or missing features.

Pull request diff:

{patch}
""".strip()

            review = self.rag_chain.review(
                query=query,
                top_k=5,
            )

            results.append(f"""
## {filename}

{review}
""".strip())

        if not results:
            return "No textual changes were available for review."

        return "\n\n".join(results)
