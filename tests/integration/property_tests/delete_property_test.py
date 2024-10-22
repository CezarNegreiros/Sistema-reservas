import pytest

from seazone.application.dtos.filter_params_dto import (
    FilterParamsPropertiesDTO,
)
from seazone.application.dtos.property_dtos import PropertyCreateDTO
from seazone.application.usecases.property.create_property import (
    CreatePropertyUseCase,
)
from seazone.application.usecases.property.delete_property import (
    DeletePropertyUseCase,
)
from seazone.application.usecases.property.list_properties import (
    ListPropertiesUseCase,
)


@pytest.mark.asyncio
async def test_delete_property(async_session):
    delete_property_use_case = DeletePropertyUseCase(async_session)
    create_property_use_case = CreatePropertyUseCase(async_session)
    list_properties_use_case = ListPropertiesUseCase(async_session)

    property_create_data = PropertyCreateDTO(
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

    created_property = await create_property_use_case.create_property(
        property_create_data
    )

    filters = FilterParamsPropertiesDTO()
    list_pre_delete = await list_properties_use_case.list_properties_use_case(
        filters
    )

    await delete_property_use_case.delete_property_use_case(
        str(created_property.id)
    )

    list_pos_delete = await list_properties_use_case.list_properties_use_case(
        filters
    )

    assert len(list_pos_delete) < len(list_pre_delete)
    assert list_pos_delete == []
