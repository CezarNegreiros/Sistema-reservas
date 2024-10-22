from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from seazone.application.dtos.filter_params_dto import (
    FilterParamsAvailabilityDTO,
    FilterParamsPropertiesDTO,
)
from seazone.application.dtos.property_dtos import (
    PropertyCreateDTO,
    PropertyResponseDTO,
)
from seazone.application.usecases.property.create_property import (
    CreatePropertyUseCase,
)
from seazone.application.usecases.property.delete_property import (
    DeletePropertyUseCase,
)
from seazone.application.usecases.property.get_properties_by_id import (
    GetPropertiesByIdUseCase,
)
from seazone.application.usecases.property.list_properties import (
    ListPropertiesUseCase,
)
from seazone.application.usecases.property.update_property import (
    UpdatePropertyUseCase,
)
from seazone.application.usecases.property.verify_availability import (
    VerifyAvailabilityUseCase,
)
from seazone.infra.database.database import get_db

router = APIRouter(prefix='/properties')


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    tags=['Properties'],
    summary='Criação de uma nova propriedade',
)
async def create_property(
    request: Request,
    property_data: PropertyCreateDTO,
    db: AsyncSession = Depends(get_db),
) -> PropertyResponseDTO:
    """
    Criação de uma nova propriedade.

    - Campos do corpo da requisição (Todos obrigatórios)
        - **title**: Id da propriedade que será reservada.
        - **address_street**: Nome do cliente que fez a reserva.
        - **address_number**: Email do cliente que fez a reserva.
        - **address_neighborhood**: Data de início da reserva.
        - **address_city**: Data de finalização da reserva.
        - **address_state**: Número de hóspedes da reserva.
        - **country**: Número de hóspedes da reserva.
        - **rooms**: Número de hóspedes da reserva.
        - **capacity**: Número de hóspedes da reserva.
        - **price_per_night**: Número de hóspedes da reserva.

    - Retorna o modelo da propriedade criada no banco
    """
    property_use_case = CreatePropertyUseCase(db)

    return await property_use_case.create_property(property_data)


@router.get(
    '',
    status_code=status.HTTP_200_OK,
    tags=['Properties'],
    summary='Listagem de propriedades',
)
async def list_properties(
    request: Request,
    filters: FilterParamsPropertiesDTO = Depends(),
    db: AsyncSession = Depends(get_db),
) -> list[PropertyResponseDTO]:
    """
    Listagem de propriedades.

    - Filtros (Todos são opcionais)
        - **neighborhood**: Bairro em que está localizada a propriedade
        - **city**: Cidade em que está localizada a propriedade
        - **state**: Estado em que está localizada a propriedade
        - **capacity**: Capacidade máxima de hóspedes da propriedade
        - **max_price**: Preço máximo, de um dia, desejado na busca pelas propriedades

    - Retorna a lista de propriedades que cumprem com as especificações enviadas nos filtros
    """

    property_use_case = ListPropertiesUseCase(db)

    return await property_use_case.list_properties_use_case(filters)


@router.get(
    '/{property_id}/details',
    status_code=status.HTTP_200_OK,
    tags=['Properties'],
    summary='Busca de propriedade pelo id',
)
async def get_property_by_id(
    request: Request,
    property_id: str,
    db: AsyncSession = Depends(get_db),
) -> PropertyResponseDTO:
    """
    Obter uma propriedade pelo id

    - Recebe o id da propriedade como parâmetro na url
    - Retorna as especificações da propriedade buscada

    """
    property_use_case = GetPropertiesByIdUseCase(db)

    return await property_use_case.get_properties_by_id(property_id)


@router.put(
    '/{property_id}',
    status_code=status.HTTP_200_OK,
    tags=['Properties'],
    summary='Atualização de propriedades',
)
async def update_property(
    request: Request,
    property_id: str,
    property_update_data: PropertyCreateDTO,
    db: AsyncSession = Depends(get_db),
) -> PropertyResponseDTO:
    """
    Atualização de Propriedade

    - Recebe o id da propriedade como parâmetro na url

    - Campos do corpo da requisição (Todos obrigatórios)
        - **title**: Id da propriedade que será reservada.
        - **address_street**: Nome do cliente que fez a reserva.
        - **address_number**: Email do cliente que fez a reserva.
        - **address_neighborhood**: Data de início da reserva.
        - **address_city**: Data de finalização da reserva.
        - **address_state**: Número de hóspedes da reserva.
        - **country**: Número de hóspedes da reserva.
        - **rooms**: Número de hóspedes da reserva.
        - **capacity**: Número de hóspedes da reserva.
        - **price_per_night**: Número de hóspedes da reserva.

    - Retorna o modelo da propriedade com as informações atualizadas
    """
    property_use_case = UpdatePropertyUseCase(db)

    return await property_use_case.update_property_use_case(
        property_id, property_update_data
    )


@router.delete(
    '/{property_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['Properties'],
    summary='Deleção de propriedades',
)
async def delete_property(
    request: Request, property_id: str, db: AsyncSession = Depends(get_db)
):
    """
    Deleção de uma Propriedade

    - Recebe o id da propriedade como parâmetro na url
    - Não retorna nada, caso o objeto seja excluído com sucesso (HTTP 204 no content)
    """
    property_use_case = DeletePropertyUseCase(db)

    await property_use_case.delete_property_use_case(property_id)


@router.get(
    '/availability',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['Properties'],
    summary='Verificação de disponibilidade de propriedades',
)
async def verify_availability(
    request: Request,
    filters: FilterParamsAvailabilityDTO = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    Verificação de disponibilidade da propriedade

    - Recebe como parâmetros para a verificação(Todos são obrigatórios):
        - property_id: id da propriedade desejada
        - start_date: Data de início possível reserva
        - end_date: Data de fim da possível reserva
        - guests_quantity: Quantidade de hóspedes da possível reserva

    - Caso a propriedade esteja disponível de acordo com os parâmetros inseridos, é retornado um HTTP 204
    - Caso algum dos parâmetros não seja enviado, é retornado um status de erro
    - Caso já exista uma reserva no intervalo de tempo inserido, é retornado um status de erro
    - Caso número de hóspedes seja maior do que a capacidade da propriedade, é retornado um status de erro
    """
    property_use_case = VerifyAvailabilityUseCase(db)

    await property_use_case.verify_availability_use_case(filters)
