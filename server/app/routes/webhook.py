from fastapi import APIRouter, Request, HTTPException
from app.utils.verifier import verify_signature
from app.queue.jobs import review_jobs
from app.workers.review_worker import process_pr
from app.config import GITHUB_WEBHOOK_SECRET


router = APIRouter()


@router.post("/github")
async def github_webhook(request: Request):

    # Raw body needed for HMAC verification
    body = await request.body()

    # GitHub signature header
    signature = request.headers.get("X-Hub-Signature-256")

    # Ensure signature header is present
    if signature is None:
        raise HTTPException(
            status_code=400, detail="Missing X-Hub-Signature-256 header"
        )

    # Ensure GitHub webhook secret is present
    if GITHUB_WEBHOOK_SECRET is None:
        raise HTTPException(
            status_code=500, detail="GitHub webhook secret not configured"
        )

    # Verify request is actually from GitHub
    if not verify_signature(body, signature, GITHUB_WEBHOOK_SECRET):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Parse JSON payload
    payload = await request.json()

    # Event type
    event = request.headers.get("X-GitHub-Event")

    print(f"\n{'=' * 50}")
    print("Event:", event)

    # Handle Pull Request events
    if event == "pull_request" and payload["action"] == "opened":

        job = review_jobs.enqueue("app.workers.review_worker.process_pr", payload)

        print(f"Job queued: {job.id}")

    return {"success": True, "message": "queued for processing"}
