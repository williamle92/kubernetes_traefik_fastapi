from fastapi import Depends, HTTPException, status
from backend.pydantic.auth import Token
from backend.models.base import get_connection
from sqlalchemy import select
from backend.models.users import User
from sqlalchemy.ext.asyncio import AsyncEngine
from passlib.hash import md5_crypt
from jose import JWTError, jwt
import datetime
from backend.configs import Configs
from fastapi.security import OAuth2PasswordBearer

oauth: OAuth2PasswordBearer = OAuth2PasswordBearer("/token")


async def verify_password_hash(password: str, hashies: str) -> bool:
    return md5_crypt.verify(password, hashies)


async def hash_password(password: str) -> str:
    return md5_crypt.hash(password)


async def create_token(username, expire: int = 1800):
    expiration: datetime.datetime = datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(
        seconds=expire
    )
    time_string = expiration.strftime("%Y-%m-%d %H:%M:%S")
    to_encode = {"sub": username, "exp": expiration}
    encoded_jwt = jwt.encode(to_encode, Configs.SECRET_KEY, algorithm=Configs.ALGORITHM)

    return Token(access_token=encoded_jwt, expiration=time_string)


async def verify_token(token=Depends(oauth), engine: AsyncEngine = Depends(get_connection)):
    try:
        payload = jwt.decode(token, Configs.SECRET_KEY, algorithms=Configs.ALGORITHM)

    except JWTError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(err),
            headers={"WWW-Authenticate": "Bearer"},
        )

    async with engine.connect() as conn:
        query = await conn.execute(select(User).where(User.email == payload.get("sub")))
        user: User = query.first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
