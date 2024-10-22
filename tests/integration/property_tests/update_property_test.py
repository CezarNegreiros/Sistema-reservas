import pytest

from seazone.application.dtos.property_dtos import PropertyCreateDTO
from seazone.application.usecases.property.create_property import (
    CreatePropertyUseCase,
)
from seazone.application.usecases.property.get_properties_by_id import (
    GetPropertiesByIdUseCase,
)
from seazone.application.usecases.property.update_property import (
    UpdatePropertyUseCase,
)


@pytest.mark.asyncio
async def test_update_property(async_session):
    update_property_use_case = UpdatePropertyUseCase(async_session)
    create_use_case = CreatePropertyUseCase(async_session)
    get_by_id_use_case = GetPropertiesByIdUseCase(async_session)
    property_create_data = PropertyCreateDTO(
        title='Casa de Férias Algarve',
        address_street='Av Github',
        address_number='2024',
        address_neighborhood='Jurerê',
        address_city='Florianópolis',
        address_state='SC',
        country='BR',
        rooms=3,
        capacity=6,
        price_per_night=120.0,
    )

    result_create = await create_use_case.create_property(property_create_data)

    property_updated_data = PropertyCreateDTO(
        title='Test Property',
        address_street='123 Main St',
        address_number='1',
        address_neighborhood='Downtown',
        address_city='Cityville',
        address_state='State',
        country='Country',
        rooms=7,
        capacity=6,
        price_per_night=500.0,
    )
    await update_property_use_case.update_property_use_case(
        str(result_create.id), property_updated_data
    )

    result = await get_by_id_use_case.get_properties_by_id(
        str(result_create.id)
    )

    assert result.title == 'Test Property'
    assert result.rooms == 7
    assert result.price_per_night == 500.0
