from fastapi import HTTPException
from seazone.application.dtos.auth_dto import CreateUserDTO
from seazone.infra.repository.user_repository import UserRepository
from passlib.context import CryptContext
from seazone.infra.services.jwt_token_service import create_access_token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user: CreateUserDTO) -> None:
        # if is_user_registered:

        user.password = self._get_password_hash(user.password)
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

    @staticmethod
    def _get_password_hash(password):
        return pwd_context.hash(password)
