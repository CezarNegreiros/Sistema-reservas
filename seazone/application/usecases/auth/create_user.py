from fastapi import HTTPException
from seazone.application.dtos.auth_dto import CreateUserDTO
from seazone.application.util.auth import get_password_hash
from seazone.infra.repository.user_repository import UserRepository
from passlib.context import CryptContext
from seazone.infra.services.jwt_token_service import create_access_token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user: CreateUserDTO) -> None:
        user_registered = await self.user_repository.get_user_by_email(
            user.email
        )

        if user_registered:
            raise HTTPException(
                status_code=400,
                detail="Usuário já cadastrado"
            )

        user.password = get_password_hash(user.password)
        try:
            await self.user_repository.create(user)
        except Exception as ex:
            raise HTTPException(
                status_code=400,
                detail=f"Não foi possível criar o usuário: {str(ex)}"
            )

        access_token = create_access_token(data={"sub": user.email})
        return {
            "status": "sucesso",
            "mensagem": "Usuário criado com sucesso",
            "access_token": access_token
        }
