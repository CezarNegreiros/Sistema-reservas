
from fastapi import Depends
from seazone.application.usecases.auth.create_user import CreateUserUseCase
from seazone.infra.database.database import AsyncSessionLocal
from seazone.infra.repository.user_repository import UserRepository
# from seazone.infra.services.jwt_token_service import JwtTokenService
from sqlalchemy.ext.asyncio import AsyncSession


# def get_jwt_token_service() -> JwtTokenService:
#     return JwtTokenService(secret_key="cezar", algorithm="HS256")


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


def user_repository(
    db: AsyncSession = Depends(get_db),
) -> UserRepository:
    return UserRepository(db_session=db)


def create_user_usecase(
    user_repository: UserRepository = Depends(user_repository),
) -> CreateUserUseCase:
    return CreateUserUseCase(user_repository=user_repository)
