from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import select
from typing import List
from backend.models import User
from backend.models.base import get_connection
from backend.pydantic.users import UserOut, UsersOut
from backend.dependencies.auth import verify_token
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.engine.row import Row


router: APIRouter = APIRouter(tags=["Users"])


@router.get("/users")
async def get_users(
    eng: AsyncEngine = Depends(get_connection),
    verified_user: User = Depends(verify_token),
) -> UsersOut:
    async with eng.connect() as conn:
        users: List = await conn.execute(select(User))

        return UsersOut(users=[UserOut.model_validate(u) for u in users.fetchall()])


@router.get("/users/{id}")
async def get_user(
    id: int,
    eng: AsyncEngine = Depends(get_connection),
    verified_user: User = Depends(verify_token),
) -> UserOut:
    async with eng.connect() as conn:
        query: CursorResult = await conn.execute(select(User).where(User.id == id))
        result: Row = query.first()

        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserOut(**result._asdict())
