from fastapi import FastAPI

from routers import router

app = FastAPI(docs_url='/')
app.include_router(router)
