from fastapi import FastAPI
from api.backend.routers.users import router as user_router
from api.backend.routers.auth import router as auth_router
from api.backend.worker.tasks import add
from pydantic import BaseModel

app: FastAPI = FastAPI(docs_url="/swagger", redoc_url="/docs", root_path="/v1/api")


app.include_router(user_router)
app.include_router(auth_router)


class MathIn(BaseModel):
    x: int
    y: int


@app.get("/math")
async def post_math(request: MathIn):
    result = add(request.x, request.y)
    return {"math": str(result)}
