from datetime import date
from typing import TypeVar

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from seazone.application.dtos.filter_params_dto import (
    FilterParamsReservationDTO,
)
from seazone.infra.repository.base_repository import BaseRepository
from seazone.domain.models import Reservation

T = TypeVar('T')


class ReservationRepository(BaseRepository):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, Reservation)

    async def list_reservations(
        self, filters_params: FilterParamsReservationDTO
    ) -> T:
        query = select(self.model)

        if filters_params.property_id:
            query = query.where(
                self.model.property_id == int(filters_params.property_id)
            )
        if filters_params.client_email:
            query = query.where(
                self.model.client_email == filters_params.client_email
            )

        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def get_reservations_by_date(
        self, start_date: date, end_date: date
    ) -> [T]:
        query = select(self.model)

        query = query.where(
            or_(
                and_(
                    self.model.end_date >= start_date,
                    self.model.start_date <= start_date,
                ),
                and_(
                    self.model.end_date >= end_date,
                    self.model.start_date <= end_date,
                ),
            )
        )

        result = await self.db_session.execute(query)
        return result.scalars().all()
