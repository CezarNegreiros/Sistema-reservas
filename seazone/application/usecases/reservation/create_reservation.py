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


class CreateReservationUseCase:
    def __init__(self, db: AsyncSession):
        self.reservation_repository = ReservationRepository(db)
        self.property_repository = PropertyRepository(db)

    async def create_reservation_use_case(
        self, reservation_data: ReservationCreateDTO
    ) -> ReservationResponseDTO:
        time_availability_reservation = (
            await self.reservation_repository.get_reservations_by_date(
                reservation_data.start_date, reservation_data.end_date
            )
        )

        if time_availability_reservation:
            raise HTTPException(
                status_code=400,
                detail='There are already reservations in that time frame',
            )

        property_data = await self.property_repository.get_by_id(
            str(reservation_data.property_id)
        )
        if property_data is None:
            raise HTTPException(
                status_code=404, detail='property not found in database'
            )
        if property_data.capacity < reservation_data.guests_quantity:
            raise HTTPException(
                status_code=400, detail='More guests than allowed'
            )

        reservation_data.total_price = (
            reservation_data.end_date - reservation_data.start_date
        ).days * property_data.price_per_night

        reservation_created = await self.reservation_repository.create(
            reservation_data
        )

        reservation_created_response = ReservationResponseDTO(
            id=reservation_created.id,
            property_id=reservation_created.property_id,
            client_name=reservation_created.client_name,
            client_email=reservation_created.client_email,
            start_date=reservation_created.start_date,
            end_date=reservation_created.end_date,
            guests_quantity=reservation_created.guests_quantity,
            total_price=reservation_created.total_price,
        )

        return reservation_created_response
