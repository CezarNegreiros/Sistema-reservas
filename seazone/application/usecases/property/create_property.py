from sqlalchemy.ext.asyncio import AsyncSession

from seazone.application.dtos.property_dtos import (
    PropertyCreateDTO,
    PropertyResponseDTO,
)
from seazone.infra.repository.property_repository import PropertyRepository


class CreatePropertyUseCase:
    def __init__(self, db: AsyncSession):
        self.property_repository = PropertyRepository(db)

    async def create_property(
        self, property: PropertyCreateDTO
    ) -> PropertyResponseDTO:
        property_created = await self.property_repository.create(property)

        property_created_response = PropertyResponseDTO(
            id=property_created.id,
            title=property_created.title,
            address_street=property_created.address_street,
            address_number=property_created.address_number,
            address_neighborhood=property_created.address_neighborhood,
            address_city=property_created.address_city,
            address_state=property_created.address_state,
            country=property_created.country,
            rooms=property_created.rooms,
            capacity=property_created.capacity,
            price_per_night=property_created.price_per_night,
        )

        return property_created_response
