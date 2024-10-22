from sqlalchemy.ext.asyncio import AsyncSession

from seazone.application.dtos.filter_params_dto import (
    FilterParamsListReservationDTO,
)
from seazone.application.dtos.reservation_dtos import ReservationResponseDTO
from seazone.infra.repository.reservation_repository import (
    ReservationRepository,
)


class ListReservationsUseCase:
    def __init__(self, db: AsyncSession):
        self.reservation_repository = ReservationRepository(db)

    async def list_reservations_use_case(
        self, filters: FilterParamsListReservationDTO
    ) -> list[ReservationResponseDTO]:
        reservations_db_result = (
            await self.reservation_repository.list_reservations(filters)
        )

        return reservations_db_result
