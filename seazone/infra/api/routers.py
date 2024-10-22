from fastapi import APIRouter

from seazone.infra.api.endpoint.property import router as property_router
from seazone.infra.api.endpoint.reservation import router as reservation_router

routers = APIRouter()

routers.include_router(property_router)
routers.include_router(reservation_router)
