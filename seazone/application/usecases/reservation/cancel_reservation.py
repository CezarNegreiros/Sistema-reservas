from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from seazone.infra.repository.reservation_repository import (
    ReservationRepository,
)


class CancelReservationUseCase:
    def __init__(self, db: AsyncSession):
        self.reservation_repository = ReservationRepository(db)

    async def cancel_reservation_use_case(self, reservation_id: str):
        reservation_db_data = await self.reservation_repository.get_by_id(
            reservation_id
        )

        if not reservation_db_data:
            raise HTTPException(
                status_code=404, detail='Property not found in database'
            )

        await self.reservation_repository.delete(reservation_id)
