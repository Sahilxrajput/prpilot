API is live at: `http://localhost:8000`  
Swagger docs: `http://localhost:8000/docs`

### Run locally (dev mode)

```bash
# Activate the virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## for starting worker

````
rq worker review_jobs --worker-class rq.worker.SimpleWorker
```
````
