from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from seazone.infra.repository.property_repository import PropertyRepository


class DeletePropertyUseCase:
    def __init__(self, db: AsyncSession):
        self.property_repository = PropertyRepository(db)

    async def delete_property_use_case(self, property_id):
        property_db_data = await self.property_repository.get_by_id(
            property_id
        )

        if not property_db_data:
            raise HTTPException(
                status_code=404, detail='Property not found in database'
            )

        await self.property_repository.delete(property_id)
