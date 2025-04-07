from fastapi import APIRouter, Request, status, Depends
from seazone.application.dtos.auth_dto import CreateUserDTO, LoginDTO

from seazone.application.usecases.auth.create_user import CreateUserUseCase
from seazone.application.usecases.auth.login import LoginUseCase
from seazone.infra.di.dependencies import create_user_usecase, login_usecase


router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_user(
    request: Request,
    user_data: CreateUserDTO,
    create_user_usecase: CreateUserUseCase = Depends(create_user_usecase)
):
    response = await create_user_usecase.execute(user_data)
    return response


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(
    request: Request,
    user_data: LoginDTO,
    login_usecase: LoginUseCase = Depends(login_usecase)
):
    response = await login_usecase.execute(user_data)
    return response
