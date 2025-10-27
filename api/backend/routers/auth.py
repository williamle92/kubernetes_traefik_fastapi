from fastapi import APIRouter, Depends, HTTPException, status
from backend.pydantic.auth import Token, OAuthRequestForm
from backend.models.base import get_connection
from sqlalchemy import select, and_, insert
from backend.models.users import User
from backend.pydantic.auth import RegisterIn, RegisterOut
from sqlalchemy.ext.asyncio import AsyncEngine
from backend.dependencies.auth import verify_password_hash, create_token, hash_password

router: APIRouter = APIRouter(tags=["Auth"])


@router.post("/token", response_model=Token, status_code=200)
async def verify_token(
    data: OAuthRequestForm = Depends(OAuthRequestForm),
    connection=Depends(get_connection),
):
    async with connection.connect() as conn:
        user: User = await conn.execute(select(User).where(and_(User.email == data.username)))
        result: User = user.first()

        if not result or not await verify_password_hash(data.password, result.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token: Token = await create_token(data.username)
        return access_token


@router.post("/register", response_model=RegisterOut, status_code=200)
async def register(request: RegisterIn, engine: AsyncEngine = Depends(get_connection)):
    hashed_password: str = await hash_password(request.password)

    async with engine.connect() as conn:
        insert_user = await conn.execute(
            insert(User)
            .values(**request.model_dump(exclude="password"), hashed_password=hashed_password)
            .returning(
                User.first_name,
                User.last_name,
                User.email,
                User.id,
                User.permission,
                User.phone_number,
                User.phone_country_code,
            )
        )
        result = insert_user.first()
        await conn.commit()
        return RegisterOut(**result._asdict())
