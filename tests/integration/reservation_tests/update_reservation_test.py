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
from seazone.application.usecases.reservation.update_reservation import (
    UpdateReservationUseCase,
)


@pytest.mark.asyncio
async def test_update_reservation(async_session):
    update_reservation_use_case = UpdateReservationUseCase(async_session)
    create_reservation_use_case = CreateReservationUseCase(async_session)
    create_property_use_case = CreatePropertyUseCase(async_session)
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

    await create_property_use_case.create_property(property_create_data)

    reservation_create_data = ReservationCreateDTO(
        property_id=1,
        client_name='Maria Pereira',
        client_email='mariapereira@example.com',
        start_date='2024-12-20',
        end_date='2024-12-27',
        guests_quantity=4,
    )

    result_create_reservation = (
        await create_reservation_use_case.create_reservation_use_case(
            reservation_create_data
        )
    )

    reservation_update_data = ReservationCreateDTO(
        property_id=1,
        client_name='Maria Pereira',
        client_email='mariapereira@example.com',
        start_date='2024-08-10',
        end_date='2024-09-10',
        guests_quantity=7,
    )

    await update_reservation_use_case.update_reservation_use_case(
        str(result_create_reservation.id), reservation_update_data
    )

    filters = FilterParamsListReservationDTO(
        client_email='mariapereira@example.com', property_id='1'
    )

    result = await list_reservations_use_case.list_reservations_use_case(
        filters
    )

    assert result[0].guests_quantity == reservation_update_data.guests_quantity
    assert result[0].start_date == reservation_update_data.start_date
    assert result[0].end_date == reservation_update_data.end_date
