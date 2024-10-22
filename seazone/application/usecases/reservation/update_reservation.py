from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from seazone.application.dtos.reservation_dtos import (
    ReservationCreateDTO,
    ReservationResponseDTO,
)
from seazone.infra.repository.property_repository import PropertyRepository
from seazone.infra.repository.reservation_repository import (
    ReservationRepository,
)


class UpdateReservationUseCase:
    def __init__(self, db: AsyncSession):
        self.reservation_repository = ReservationRepository(db)
        self.property_repository = PropertyRepository(db)

    async def update_reservation_use_case(
        self, reservation_id: str, reservation_data: ReservationCreateDTO
    ) -> ReservationResponseDTO:
        reservation_db_response = await self.reservation_repository.get_by_id(
            reservation_id
        )

        if not reservation_db_response:
            raise HTTPException(
                status_code=404, detail='Property not found in database'
            )

        property_data = await self.property_repository.get_by_id(
            str(reservation_data.property_id)
        )

        reservation_data.total_price = (
            reservation_data.end_date - reservation_data.start_date
        ).days * property_data.price_per_night

        reservation_updated_data = await self.reservation_repository.update(
            reservation_id, reservation_data
        )

        reservation_updated_response = ReservationResponseDTO(
            id=reservation_updated_data.id,
            property_id=reservation_updated_data.property_id,
            client_name=reservation_updated_data.client_name,
            client_email=reservation_updated_data.client_email,
            start_date=reservation_updated_data.start_date,
            end_date=reservation_updated_data.end_date,
            guests_quantity=reservation_updated_data.guests_quantity,
            total_price=reservation_updated_data.total_price,
        )

        return reservation_updated_response
