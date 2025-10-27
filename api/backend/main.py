from fastapi import FastAPI
from backend.routers.users import router as user_router
from backend.routers.auth import router as auth_router
from backend.worker.tasks import add

app: FastAPI = FastAPI(docs_url="/swagger", redoc_url="/")


app.include_router(user_router)
app.include_router(auth_router)


@app.get("/math")
async def home():
    result = add.delay(4, 4)
    return {"math": str(result)}
