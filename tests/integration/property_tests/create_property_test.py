import pytest

from seazone.application.dtos.property_dtos import PropertyCreateDTO
from seazone.application.usecases.property.create_property import (
    CreatePropertyUseCase,
)


@pytest.mark.asyncio
async def test_create_property(async_session):
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
    property_response = await create_property_use_case.create_property(
        property_dto
    )

    assert property_response.title == property_dto.title
    assert property_response.address_street == property_dto.address_street
    assert property_response.price_per_night == property_dto.price_per_night
