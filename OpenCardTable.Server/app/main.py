from fastapi import FastAPI

app = FastAPI(title="Open Card Table")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {
        "name": "Open Card Table",
        "status": "ok",
        "version": "0.0.1",
    }
