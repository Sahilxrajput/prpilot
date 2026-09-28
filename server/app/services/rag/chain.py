import os

from huggingface_hub import InferenceClient

from app.services.rag.retriever import CodeRetriever


class RAGChain:

    def __init__(self):
        self.retriever = CodeRetriever()

        token = os.getenv("HF_TOKEN")

        if not token:
            raise RuntimeError("HF_TOKEN is missing")

        self.model = os.getenv("LLM_MODEL", "Qwen/Qwen2.5-Coder-32B-Instruct")

        self.client = InferenceClient(api_key=token)

    def review(self, query: str, top_k: int = 5) -> str:

        chunks = self.retriever.retrieve(query=query, top_k=top_k)

        if not chunks:
            return "No relevant code was found."

        context = self._build_context(chunks)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._system_prompt()},
                {
                    "role": "user",
                    "content": self._build_user_prompt(query=query, context=context),
                },
            ],
            temperature=0.1,
            max_tokens=2000,
        )

        return response.choices[0].message.content

    def _build_context(self, chunks: list[dict]) -> str:

        context_parts = []

        for i, chunk in enumerate(chunks, start=1):

            context_parts.append(f"""
--- Code Chunk {i} ---

File: {chunk.get("file")}
Symbol: {chunk.get("name")}
Similarity: {chunk.get("score")}

Code:

{chunk.get("content")}
""".strip())

        return "\n\n".join(context_parts)

    def _build_user_prompt(self, query: str, context: str) -> str:

        return f"""
Review the repository code below.

Review request:
{query}

Retrieved repository context:
{context}

Analyze the code carefully and report only genuine issues.
""".strip()

    def _system_prompt(self) -> str:

        return """
You are a senior software engineer performing a rigorous code review.

Your job is to identify REAL problems in the provided code.

IMPORTANT RULES:

1. Only report issues that are directly supported by the code.

2. Do NOT invent behavior, files, functions, variables, or
   application requirements.

3. Do NOT treat normal implementation choices as vulnerabilities.

4. Do NOT report hypothetical problems unless the provided code
   clearly demonstrates that the problem can occur.

5. Do NOT treat missing features as bugs unless the review request
   explicitly requires that feature.

6. Do NOT report style preferences as bugs.

7. Do NOT recommend changes merely because another implementation
   might be cleaner.

8. Before reporting an issue, ask:
   "Can I point to concrete code that demonstrates this problem?"

   If the answer is no, do not report it.

9. Environment variables, logging, error handling, framework usage,
   and API design are NOT automatically security problems.

10. If the code is correct, explicitly say that no significant issue
    was found.

SEVERITY:

Critical:
A severe vulnerability or correctness issue with major impact.

High:
A serious, demonstrable security or correctness issue.

Medium:
A real issue that can cause meaningful incorrect behavior,
security problems, or reliability problems.

Low:
A minor but demonstrable issue.

Do not assign severity based on how interesting an issue sounds.

For every finding use:

### Finding N

- Severity:
- File:
- Symbol:
- Problem:
- Evidence:
- Why it matters:
- Suggested fix:

The "Evidence" field must point to the actual code or behavior
supporting the finding.

If no genuine issue exists, return:

## Findings

No significant issues found in the reviewed code.

Do not manufacture findings just to make the review look useful.

Finally provide:

## Conclusion

Summarize only what can be concluded from the changed code and
the retrieved repository context.

Do not claim that the entire repository is correct or secure.
Do not make conclusions about code that was not provided.
""".strip()
