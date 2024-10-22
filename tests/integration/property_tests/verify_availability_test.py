import pytest
from fastapi import HTTPException

from seazone.application.dtos.filter_params_dto import (
    FilterParamsAvailabilityDTO,
)
from seazone.application.dtos.property_dtos import PropertyCreateDTO
from seazone.application.dtos.reservation_dtos import ReservationCreateDTO
from seazone.application.usecases.property.create_property import (
    CreatePropertyUseCase,
)
from seazone.application.usecases.property.verify_availability import (
    VerifyAvailabilityUseCase,
)
from seazone.application.usecases.reservation.create_reservation import (
    CreateReservationUseCase,
)


@pytest.mark.asyncio
async def test_verify_availability(async_session):
    create_property_use_case = CreatePropertyUseCase(async_session)
    verify_availability_use_case = VerifyAvailabilityUseCase(async_session)

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

    filters = FilterParamsAvailabilityDTO(
        property_id='1',
        start_date='2024-10-20',
        end_date='2024-10-30',
        guests_quantity='5',
    )

    await verify_availability_use_case.verify_availability_use_case(filters)


@pytest.mark.asyncio
async def test_verify_availability_not_avaliable(async_session):
    create_property_use_case = CreatePropertyUseCase(async_session)
    verify_availability_use_case = VerifyAvailabilityUseCase(async_session)
    create_reservation_use_case = CreateReservationUseCase(async_session)

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

    await create_property_use_case.create_property(property_dto)

    reservation_create_data = ReservationCreateDTO(
        property_id=1,
        client_name='Maria Pereira',
        client_email='mariapereira@example.com',
        start_date='2024-12-20',
        end_date='2024-12-27',
        guests_quantity=4,
    )

    await create_reservation_use_case.create_reservation_use_case(
        reservation_create_data
    )

    filters = FilterParamsAvailabilityDTO(
        property_id='1',
        start_date='2024-12-25',
        end_date='2024-12-30',
        guests_quantity='5',
    )

    with pytest.raises(HTTPException) as exc_info:
        await verify_availability_use_case.verify_availability_use_case(
            filters
        )

    assert exc_info.value.status_code == 400
    assert (
        exc_info.value.detail
        == 'There are already reservations in that time frame'
    )
