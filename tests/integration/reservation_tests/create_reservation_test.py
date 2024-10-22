import pytest

from seazone.application.dtos.property_dtos import PropertyCreateDTO
from seazone.application.dtos.reservation_dtos import ReservationCreateDTO
from seazone.application.usecases.property.create_property import (
    CreatePropertyUseCase,
)
from seazone.application.usecases.reservation.create_reservation import (
    CreateReservationUseCase,
)


@pytest.mark.asyncio
async def test_create_reservation(async_session):
    create_property_use_case = CreatePropertyUseCase(async_session)
    create_reservation_use_case = CreateReservationUseCase(async_session)

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

    created_property = await create_property_use_case.create_property(
        property_create_data
    )

    reservation_create_data = ReservationCreateDTO(
        property_id=1,
        client_name='Maria Pereira',
        client_email='mariapereira@example.com',
        start_date='2024-12-20',
        end_date='2024-12-27',
        guests_quantity=4,
    )

    created_reservation = (
        await create_reservation_use_case.create_reservation_use_case(
            reservation_create_data
        )
    )

    assert created_reservation.property_id == created_property.id
    assert (
        created_reservation.guests_quantity
        == reservation_create_data.guests_quantity
    )
    assert created_reservation.start_date == reservation_create_data.start_date
