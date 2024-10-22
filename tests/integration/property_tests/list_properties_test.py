import pytest

from seazone.application.dtos.filter_params_dto import (
    FilterParamsPropertiesDTO,
)
from seazone.application.dtos.property_dtos import PropertyCreateDTO
from seazone.application.usecases.property.create_property import (
    CreatePropertyUseCase,
)
from seazone.application.usecases.property.list_properties import (
    ListPropertiesUseCase,
)


@pytest.mark.asyncio
async def test_list_properties_without_filters(async_session):
    create_use_case = CreatePropertyUseCase(async_session)

    property_create_data = PropertyCreateDTO(
        title='Test Property',
        address_street='123 Main St',
        address_number='1',
        address_neighborhood='Downtown',
        address_city='Cityville',
        address_state='State',
        country='Country',
        rooms=3,
        capacity=6,
        price_per_night=100.0,
    )
    await create_use_case.create_property(property_create_data)

    property_create_data = PropertyCreateDTO(
        title='Propriedade Teste',
        address_street='Av efigenio sales',
        address_number='1',
        address_neighborhood='Parque 10',
        address_city='Manaus',
        address_state='Amazonas',
        country='BR',
        rooms=3,
        capacity=6,
        price_per_night=100.0,
    )

    await create_use_case.create_property(property_create_data)

    # Executa o caso de uso de listagem
    filters = FilterParamsPropertiesDTO(
        city=None,
        state=None,
        capacity=None,
        neighborhood=None,
        max_price=None,
    )

    list_use_case = ListPropertiesUseCase(async_session)

    properties = await list_use_case.list_properties_use_case(filters)

    # Verifica se a propriedade criada está na lista
    assert len(properties) > 1
    assert properties[0].title == 'Test Property'


# Executa o caso de uso de listagem
@pytest.mark.asyncio
async def test_list_properties_with_filters(async_session):
    create_use_case = CreatePropertyUseCase(async_session)
    list_use_case = ListPropertiesUseCase(async_session)

    property_dto = PropertyCreateDTO(
        title='Test Property',
        address_street='123 Main St',
        address_number='1',
        address_neighborhood='Downtown',
        address_city='Cityville',
        address_state='State',
        country='Country',
        rooms=3,
        capacity=6,
        price_per_night=100.0,
    )

    await create_use_case.create_property(property_dto)

    property_dto = PropertyCreateDTO(
        title='Propriedade Teste',
        address_street='Av efigenio sales',
        address_number='1',
        address_neighborhood='Parque 10',
        address_city='Manaus',
        address_state='Amazonas',
        country='BR',
        rooms=3,
        capacity=6,
        price_per_night=100.0,
    )

    await create_use_case.create_property(property_dto)

    filters = FilterParamsPropertiesDTO(
        city='Manaus',
        capacity=5,
    )

    properties = await list_use_case.list_properties_use_case(filters)

    # Verifica se a propriedade criada está na lista
    assert len(properties) == 1
    assert properties[0].title == 'Propriedade Teste'
