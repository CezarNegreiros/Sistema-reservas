from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from seazone.application.dtos.filter_params_dto import (
    FilterParamsAvailabilityDTO,
)
from seazone.infra.repository.property_repository import PropertyRepository
from seazone.infra.repository.reservation_repository import (
    ReservationRepository,
)


class VerifyAvailabilityUseCase:
    def __init__(self, db: AsyncSession):
        self.property_repository = PropertyRepository(db)
        self.reservation_repository = ReservationRepository(db)

    async def verify_availability_use_case(
        self, filters: FilterParamsAvailabilityDTO
    ):
        if (
            filters.property_id is None
            or filters.start_date is None
            or filters.end_date is None
            or filters.guests_quantity is None
        ):
            raise HTTPException(
                status_code=400,
                detail='The property_id, start_date, end_date and guests_quantity fields must be filled in',
            )

        time_availability_reservation = (
            await self.reservation_repository.get_reservations_by_date(
                filters.start_date, filters.end_date
            )
        )

        if time_availability_reservation:
            raise HTTPException(
                status_code=400,
                detail='There are already reservations in that time frame',
            )

        guest_capacity_of_property = await self.property_repository.get_by_id(
            str(filters.property_id)
        )

        if guest_capacity_of_property.capacity < filters.guests_quantity:
            raise HTTPException(
                status_code=400,
                detail='More guests than allowed on this property',
            )
