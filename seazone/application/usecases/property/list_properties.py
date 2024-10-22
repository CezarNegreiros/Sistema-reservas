from sqlalchemy.ext.asyncio import AsyncSession

from seazone.application.dtos.filter_params_dto import (
    FilterParamsPropertiesDTO,
)
from seazone.application.dtos.property_dtos import PropertyResponseDTO
from seazone.infra.repository.property_repository import PropertyRepository


class ListPropertiesUseCase:
    def __init__(self, db: AsyncSession):
        self.property_repository = PropertyRepository(db)

    async def list_properties_use_case(
        self, filters: FilterParamsPropertiesDTO
    ) -> list[PropertyResponseDTO]:
        properties_db_result = await self.property_repository.list_properties(
            filters
        )

        return properties_db_result
