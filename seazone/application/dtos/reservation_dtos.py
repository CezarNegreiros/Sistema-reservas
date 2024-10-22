from datetime import date
from typing import Optional

from pydantic import BaseModel, field_validator


class ReservationCreateDTO(BaseModel):
    property_id: int
    client_name: str
    client_email: str
    start_date: date
    end_date: date
    guests_quantity: int
    total_price: Optional[float] = None

    @field_validator('end_date', mode='after')
    def check_dates(cls, end_date, values):
        start_date = values.data['start_date']
        if start_date and end_date <= start_date:
            raise ValueError('The end date must be later than the start date.')
        return end_date

    class Config:
        json_schema_extra = {
            'example': {
                'property_id': 1,
                'client_name': 'John Doe',
                'client_email': 'johndoe@example.com',
                'start_date': '2024-12-20',
                'end_date': '2024-12-27',
                'guests_quantity': 2,
            }
        }


class ReservationResponseDTO(ReservationCreateDTO):
    id: int

    class Config:
        json_schema_extra = {
            'example': {
                'id': 1,
                'property_id': 1,
                'client_name': 'John Doe',
                'client_email': 'johndoe@example.com',
                'start_date': '2024-12-20',
                'end_date': '2024-12-27',
                'guests_quantity': 2,
            }
        }
