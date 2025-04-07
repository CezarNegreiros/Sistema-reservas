from sqlalchemy import select
from seazone.domain.models import User
from seazone.infra.repository.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseRepository):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, User)

    async def get_user_by_email(self, email: str) -> User:
        query = select(User).where(User.email == email)
        result = await self.db_session.execute(query)
        return result.scalars().first()
