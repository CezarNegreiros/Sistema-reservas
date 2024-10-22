from pydantic import BaseModel


class PropertyCreateDTO(BaseModel):
    title: str
    address_street: str
    address_number: str
    address_neighborhood: str
    address_city: str
    address_state: str
    country: str
    rooms: int
    capacity: int
    price_per_night: float

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'Casa de praia ponta negra',
                'address_street': 'Av Coronel Teixeira',
                'address_number': '3010',
                'address_neighborhood': 'Ponta Negra',
                'address_city': 'Manaus',
                'address_state': 'AM',
                'country': 'BR',
                'rooms': 3,
                'capacity': 6,
                'price_per_night': 150.00,
            }
        }


class PropertyResponseDTO(PropertyCreateDTO):
    id: int

    class Config:
        json_schema_extra = {
            'example': {
                'id': 1,
                'title': 'Casa de praia ponta negra',
                'address_street': 'Av Coronel Teixeira',
                'address_number': '3010',
                'address_neighborhood': 'Ponta Negra',
                'address_city': 'Manaus',
                'address_state': 'AM',
                'country': 'BR',
                'rooms': 3,
                'capacity': 6,
                'price_per_night': 150.00,
            }
        }
