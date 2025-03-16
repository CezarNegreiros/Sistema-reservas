from fastapi import APIRouter, Request, status, Depends
from seazone.application.dtos.auth_dto import CreateUserDTO
from sqlalchemy.ext.asyncio import AsyncSession

from seazone.application.usecases.auth.create_user import CreateUserUseCase
from seazone.infra.database.database import get_db
from seazone.infra.di.dependencies import create_user_usecase


router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_user(
    request: Request,
    user_data: CreateUserDTO,
    db: AsyncSession = Depends(get_db),
    create_user_usecase: CreateUserUseCase = Depends(create_user_usecase)
):
    response = await create_user_usecase.execute(user_data)
    return response
