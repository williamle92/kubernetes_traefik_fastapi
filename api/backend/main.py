from fastapi import FastAPI
from api.backend.routers.users import router as user_router
from api.backend.routers.auth import router as auth_router
from api.backend.worker.tasks import add

app: FastAPI = FastAPI(docs_url="/swagger", redoc_url="/docs", root_path="/v1/api")


app.include_router(user_router)
app.include_router(auth_router)


@app.get("/math")
async def home():
    result = add.delay(4, 4)
    return {"math": str(result)}
