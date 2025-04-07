from fastapi import HTTPException, status
from seazone.application.dtos.auth_dto import LoginDTO
from seazone.application.util.auth import verify_password
from seazone.infra.repository.user_repository import UserRepository
from seazone.infra.services.jwt_token_service import create_access_token


class LoginUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user: LoginDTO) -> None:
        user_registered = await self.user_repository.get_user_by_email(
            user.email
        )

        if not user_registered:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário não cadastrado"
            )

        if not verify_password(user.password, user_registered.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Senha incorreta"
            )

        access_token = create_access_token(
            data={
                "email": user.email,
                "user_id": user_registered.id
            })

        return {
            "status": "sucesso",
            "mensagem": "Usuário logado com sucesso",
            "access_token": access_token
        }
