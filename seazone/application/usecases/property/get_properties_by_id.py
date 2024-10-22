from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from seazone.application.dtos.property_dtos import PropertyResponseDTO
from seazone.infra.repository.property_repository import PropertyRepository


class GetPropertiesByIdUseCase:
    def __init__(self, db: AsyncSession):
        self.property_repository = PropertyRepository(db)

    async def get_properties_by_id(
        self, property_id: str
    ) -> PropertyResponseDTO:
        db_property_data = await self.property_repository.get_by_id(
            property_id
        )

        if not db_property_data:
            raise HTTPException(
                status_code=404, detail='Property not found in database'
            )

        property_response = PropertyResponseDTO(
            id=db_property_data.id,
            title=db_property_data.title,
            address_street=db_property_data.address_street,
            address_number=db_property_data.address_number,
            address_neighborhood=db_property_data.address_neighborhood,
            address_city=db_property_data.address_city,
            address_state=db_property_data.address_state,
            country=db_property_data.country,
            rooms=db_property_data.rooms,
            capacity=db_property_data.capacity,
            price_per_night=db_property_data.price_per_night,
        )

        return property_response
