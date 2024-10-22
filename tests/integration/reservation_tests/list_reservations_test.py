import pytest

from seazone.application.dtos.filter_params_dto import (
    FilterParamsListReservationDTO,
)
from seazone.application.dtos.property_dtos import PropertyCreateDTO
from seazone.application.dtos.reservation_dtos import ReservationCreateDTO
from seazone.application.usecases.property.create_property import (
    CreatePropertyUseCase,
)
from seazone.application.usecases.reservation.create_reservation import (
    CreateReservationUseCase,
)
from seazone.application.usecases.reservation.list_reservations import (
    ListReservationsUseCase,
)


@pytest.mark.asyncio
async def test_list_reservations_without_filters(async_session):
    create_property_use_case = CreatePropertyUseCase(async_session)
    create_reservation_use_case = CreateReservationUseCase(async_session)
    list_reservations_use_case = ListReservationsUseCase(async_session)

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

    reservation_create_data_1 = ReservationCreateDTO(
        property_id=1,
        client_name='Maria Pereira',
        client_email='mariapereira@example.com',
        start_date='2024-12-20',
        end_date='2024-12-27',
        guests_quantity=4,
    )

    await create_reservation_use_case.create_reservation_use_case(
        reservation_create_data_1
    )

    reservation_create_data_2 = ReservationCreateDTO(
        property_id=1,
        client_name='Maria Pereira',
        client_email='mariapereira@example.com',
        start_date='2024-05-10',
        end_date='2024-05-18',
        guests_quantity=4,
    )

    await create_reservation_use_case.create_reservation_use_case(
        reservation_create_data_2
    )

    filters = FilterParamsListReservationDTO()

    reservations_list_result = (
        await list_reservations_use_case.list_reservations_use_case(filters)
    )

    assert len(reservations_list_result) > 1
    assert (
        reservations_list_result[0].start_date
        == reservation_create_data_1.start_date
    )
    assert (
        reservations_list_result[1].start_date
        == reservation_create_data_2.start_date
    )
