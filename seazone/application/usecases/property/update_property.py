from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from seazone.application.dtos.property_dtos import (
    PropertyCreateDTO,
    PropertyResponseDTO,
)
from seazone.infra.repository.property_repository import PropertyRepository


class UpdatePropertyUseCase:
    def __init__(self, db: AsyncSession):
        self.property_repository = PropertyRepository(db)

    async def update_property_use_case(
        self, property_id: str, property_data: PropertyCreateDTO
    ) -> PropertyResponseDTO:
        property_db_response = await self.property_repository.get_by_id(
            property_id
        )

        if not property_db_response:
            raise HTTPException(
                status_code=404, detail='Property not found in database'
            )

        property_updated_data = await self.property_repository.update(
            property_id, property_data
        )

        property_updated_response = PropertyResponseDTO(
            id=property_updated_data.id,
            title=property_updated_data.title,
            address_street=property_updated_data.address_street,
            address_number=property_updated_data.address_number,
            address_neighborhood=property_updated_data.address_neighborhood,
            address_city=property_updated_data.address_city,
            address_state=property_updated_data.address_state,
            country=property_updated_data.country,
            rooms=property_updated_data.rooms,
            capacity=property_updated_data.capacity,
            price_per_night=property_updated_data.price_per_night,
        )

        return property_updated_response
