from fastapi import FastAPI
from api.backend.routers.users import router as user_router
from api.backend.routers.auth import router as auth_router
from api.backend.worker.tasks import add
from pydantic import BaseModel
from fastapi.openapi.docs import get_redoc_html
from fastapi.responses import HTMLResponse

app: FastAPI = FastAPI(docs_url="/swagger", redoc_url=None, title="Hyperion")


app.include_router(user_router)
app.include_router(auth_router)


class MathIn(BaseModel):
    x: int
    y: int


@app.get("/math")
async def post_math(request: MathIn):
    result = add(request.x, request.y)
    return {"math": str(result)}


@app.get("/docs", include_in_schema=False)
async def redoc_html() -> HTMLResponse:
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title,
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js",
    )
