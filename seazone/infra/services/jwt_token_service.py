from datetime import datetime, timedelta, timezone
from jwt import encode
from seazone.infra.settings.settings import settings


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(
        to_encode,
        settings.SECRET,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt
