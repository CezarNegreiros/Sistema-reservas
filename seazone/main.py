from fastapi import FastAPI
from pydantic_core import ValidationError

from seazone.infra.api.routers import routers as v1_routers
from seazone.infra.middleware.exception_middleware import ExceptionMiddleware

app = FastAPI()


app.include_router(v1_routers)

app.add_exception_handler(Exception, ExceptionMiddleware.exception_handler)
app.add_exception_handler(
    ValidationError, ExceptionMiddleware.exception_handler
)
