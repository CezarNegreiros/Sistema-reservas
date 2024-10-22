from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from seazone.application.dtos.filter_params_dto import (
    FilterParamsPropertiesDTO,
)
from seazone.infra.repository.base_repository import BaseRepository
from seazone.models.models import Property

T = TypeVar('T')


class PropertyRepository(BaseRepository):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, Property)

    async def list_properties(
        self, filters_params: FilterParamsPropertiesDTO
    ) -> T:
        query = select(self.model)

        if filters_params.city:
            query = query.where(
                self.model.address_city.ilike(f'%{filters_params.city}%')
            )
        if filters_params.neighborhood:
            query = query.where(
                self.model.address_neighborhood.ilike(
                    f'%{filters_params.neighborhood}%'
                )
            )
        if filters_params.state:
            query = query.where(
                self.model.address_state.ilike(f'%{filters_params.state}%')
            )
        if filters_params.capacity:
            query = query.where(self.model.capacity >= filters_params.capacity)
        if filters_params.max_price:
            query = query.where(
                self.model.price_per_night <= filters_params.max_price
            )

        result = await self.db_session.execute(query)
        return result.scalars().all()
