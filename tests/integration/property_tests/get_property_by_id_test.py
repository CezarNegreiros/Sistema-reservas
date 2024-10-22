import pytest

from seazone.application.dtos.property_dtos import PropertyCreateDTO
from seazone.application.usecases.property.create_property import (
    CreatePropertyUseCase,
)
from seazone.application.usecases.property.get_properties_by_id import (
    GetPropertiesByIdUseCase,
)


@pytest.mark.asyncio
async def test_get_properties_by_id(async_session):
    get_property_by_id_use_case = GetPropertiesByIdUseCase(async_session)
    create_property_use_case = CreatePropertyUseCase(async_session)
    property_dto = PropertyCreateDTO(
        title='Test Property',
        address_street='123 Main St',
        address_number='2000',
        address_neighborhood='Downtown',
        address_city='Cityville',
        address_state='State',
        country='Country',
        rooms=3,
        capacity=6,
        price_per_night=100.0,
    )

    # Execute o caso de uso
    property_created1 = await create_property_use_case.create_property(
        property_dto
    )
    property_created2 = await create_property_use_case.create_property(
        property_dto
    )

    result = await get_property_by_id_use_case.get_properties_by_id(
        str(property_created2.id)
    )

    assert result.id != property_created1.id
    assert result.id == property_created2.id
    assert result.rooms == property_created2.rooms
