from fastapi import FastAPI
from routers import snapshots

app = FastAPI(docs_url='/')
app.include_router(snapshots.router)
