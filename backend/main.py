from fastapi import FastAPI

app = FastAPI(title="PGBMS API", version="0.1.0")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "PGBMS API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

    