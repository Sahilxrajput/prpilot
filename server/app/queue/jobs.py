from redis import Redis
from rq import Queue

from app.config import REDIS_HOST, REDIS_PORT

redis_conn = Redis(host=REDIS_HOST, port=int(REDIS_PORT))

review_jobs = Queue("review_jobs", connection=redis_conn)

embed_jobs = Queue("embed_jobs", connection=redis_conn)
