from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from seazone.application.dtos.filter_params_dto import (
    FilterParamsListReservationDTO,
)
from seazone.application.dtos.reservation_dtos import (
    ReservationCreateDTO,
    ReservationResponseDTO,
)
from seazone.application.usecases.reservation.cancel_reservation import (
    CancelReservationUseCase,
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
from seazone.infra.database.database import get_db
from seazone.infra.middleware.verification_token_middleware import (
    verification_token
)

router = APIRouter(prefix='/reservations')


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    tags=['Reservation'],
    summary='Criação de uma nova reserva',
)
@verification_token
async def create_reservation(
    request: Request,
    reservation_data: ReservationCreateDTO,
    db: AsyncSession = Depends(get_db),
) -> ReservationResponseDTO:
    """
    Criação de uma nova reserva.

    - Campos do corpo da requisição:
        - **property_id**: Id da propriedade que será reservada.
        - **client_name**: Nome do cliente que fez a reserva.
        - **client_email**: Email do cliente que fez a reserva.
        - **start_date**: Data de início da reserva.
        - **end_date**: Data de finalização da reserva.
        - **guests_quantity**: Número de hóspedes da reserva.

    - Retorna os detalhes da reserva criada.
    """
    reservation_use_case = CreateReservationUseCase(db)

    return await reservation_use_case.create_reservation_use_case(
        reservation_data
    )


@router.get(
    '',
    status_code=status.HTTP_200_OK,
    tags=['Reservation'],
    summary='Listagem reservas',
)
@verification_token
async def list_reservations(
    request: Request,
    filters: FilterParamsListReservationDTO = Depends(),
    db: AsyncSession = Depends(get_db),
) -> list[ReservationResponseDTO]:
    """
    Listagem de reservas.

    - Filtros (Todos são opcionais)
        - property_id: Id da propriedade vinculada à reserva
        - client_email: Email de quem fez a reserva

    - Retorna a lista de reservas que cumprem com as especificações enviadas
    nos filtros
    """
    reservation_use_case = ListReservationsUseCase(db)

    return await reservation_use_case.list_reservations_use_case(filters)


@router.delete(
    '/{reservation_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['Reservation'],
    summary='Cancelamento de uma reserva',
)
@verification_token
async def cancel_reservation(
    request: Request, reservation_id: str, db: AsyncSession = Depends(get_db)
):
    """
    Cancelamento de uma Reserva

    - Recebe o id da reserva como parâmetro na url
    - Não retorna nada, caso a reserva seja cancelada (excluída) com sucesso
    (HTTP 204 no content)
    """

    reservation_use_case = CancelReservationUseCase(db)

    await reservation_use_case.cancel_reservation_use_case(reservation_id)


@router.put(
    '/{reservation_id}',
    status_code=status.HTTP_200_OK,
    tags=['Reservation'],
    summary='Atualização de uma reserva',
)
@verification_token
async def update_reservation(
    request: Request,
    reservation_id: str,
    reservation_update_data: ReservationCreateDTO,
    db: AsyncSession = Depends(get_db),
) -> ReservationResponseDTO:
    """
    Criação de uma nova reserva.

    - Recebe o id da reserva como parâmetro na url

    - Campos do corpo da requisição:
        - **property_id**: Id da propriedade que será reservada.
        - **client_name**: Nome do cliente que fez a reserva.
        - **client_email**: Email do cliente que fez a reserva.
        - **start_date**: Data de início da reserva.
        - **end_date**: Data de finalização da reserva.
        - **guests_quantity**: Número de hóspedes da reserva.

    - Retorna os detalhes atualizados da reserva.
    """
    reservation_use_case = UpdateReservationUseCase(db)

    return await reservation_use_case.update_reservation_use_case(
        reservation_id, reservation_update_data
    )
