from rq import Connections
from rq import Queue
from rq import SimpleWorker

from app.queue.jobs import redis_conn

with Connections(redis_conn):

    worker = SimpleWorker(
        [
            Queue("review_jobs"),
            Queue("embed_jobs"),
        ]
    )

    worker.work()
