from seazone.domain.models import User
from seazone.infra.repository.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseRepository):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, User)
