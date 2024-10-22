import re

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from seazone.application.dtos.error_dto import ServiceError


class ExceptionMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app
        self.app.add_exception_handler(Exception, self.exception_handler)

    @staticmethod
    async def exception_handler(
        request: Request, ex: Exception
    ) -> JSONResponse:
        # Handle custom ServiceError
        if isinstance(ex, ServiceError):
            formatted_errors = [
                {
                    'name': ex.status_code,
                    'errors': f'{ex.status_code}: {ex.message}',
                }
            ]
            return JSONResponse(
                status_code=ex.status_code, content=formatted_errors
            )

        # Handle FastAPI RequestValidationError
        if isinstance(ex, RequestValidationError):
            errors = ex.errors()
            formatted_errors = [
                {
                    'name': ' -> '.join([
                        str(loc_part) for loc_part in err['loc']
                    ])
                    if err['loc']
                    else 'general',
                    'errors': [err['msg']],
                }
                for err in errors
            ]
            return JSONResponse(status_code=422, content=formatted_errors)

        # Handle Pydantic ValidationError
        if isinstance(ex, ValidationError):
            errors = ex.errors()
            formatted_errors = [
                {
                    'name': ' -> '.join([
                        str(loc_part) for loc_part in err['loc']
                    ])
                    if err['loc']
                    else 'general',
                    'errors': [err['msg']],
                }
                for err in errors
            ]
            return JSONResponse(status_code=422, content=formatted_errors)

        # Handle AttributeError
        if isinstance(ex, AttributeError):
            error_message = str(ex)
            formatted_errors = [
                {'name': 422, 'errors': f'Atributo com erro: {error_message}'}
            ]
            return JSONResponse(status_code=422, content=formatted_errors)

        # Handle ResponseValidationError
        if isinstance(ex, ResponseValidationError):
            error_message = str(ex)
            error_inputs = re.findall(r"'input':\s*({.*?})", error_message)
            input_error = (
                error_inputs[0] if error_inputs else 'No input error found'
            )
            formatted_errors = [
                {'name': 401, 'errors': f'Atributo com erro: {input_error}'}
            ]
            return JSONResponse(status_code=401, content=formatted_errors)

        # Generic error response
        formatted_errors = [{'name': 500, 'errors': 'Error not Mapped'}]
        return JSONResponse(status_code=500, content=formatted_errors)
