from datetime import date
from typing import Optional

from fastapi import Query
from pydantic import BaseModel


class FilterParamsPropertiesDTO(BaseModel):
    neighborhood: Optional[str] = Query(None)
    city: Optional[str] = Query(None)
    state: Optional[str] = Query(None)
    capacity: Optional[int] = Query(None)
    max_price: Optional[float] = Query(None)


class FilterParamsReservationDTO(BaseModel):
    property_id: Optional[str] = Query(None)
    client_name: Optional[str] = Query(None)
    client_email: Optional[str] = Query(None)
    start_date: Optional[date] = Query(None)
    end_date: Optional[date] = Query(None)
    guests_quantity: Optional[int] = Query(None)


class FilterParamsAvailabilityDTO(BaseModel):
    property_id: Optional[str] = Query(None)
    start_date: Optional[date] = Query(None)
    end_date: Optional[date] = Query(None)
    guests_quantity: Optional[int] = Query(None)


class FilterParamsListReservationDTO(BaseModel):
    property_id: Optional[str] = Query(None)
    client_email: Optional[str] = Query(None)
