from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel

from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

API_TITLE = "API"
API_DESCRIPTION = "API"
API_VERSION = "0.1"


class ApiInfo(BaseModel):
    title: str
    description: str
    version: str

    class Config:
        json_schema_extra = {
            "example": {
                "title": API_TITLE,
                "description": API_DESCRIPTION,
                "version": API_VERSION,
            }
        }


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="API",
        version="1.0.0",
        description="API version 1.0.0",
        routes=app.routes,
        servers=_get_servers(),
    )
    openapi_schema["info"]["contact"] = {"name": "", "email": ""}
    openapi_schema["info"]["x-logo"] = {"url": ""}
    openapi_schema["x-readme"] = {
        "samples-languages": ["curl", "node", "javascript", "python"]
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def _get_servers():
    return [{"url": "http://0.0.0.0:8082"}]


app.openapi = custom_openapi
"""
# order of middleware matters! first middleware called is the last one added
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(MainMiddleware)
app.add_middleware(RequestEnrichmentMiddleware)

# exception handlers run AFTER the middlewares!
# Handles API error responses
app.add_exception_handler(Exception, custom_exception_handler)
"""


# Overrides FastAPI error responses, eg: authorization, not found
# app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)
# Overrides default Pydantic request validation errors
# app.add_exception_handler(RequestValidationError, validation_exception_handler)


def get_api_info() -> ApiInfo:
    return ApiInfo(title=API_VERSION, description=API_DESCRIPTION, version=API_VERSION)


@app.get(
    "/",
    response_model=ApiInfo,
)
def root():
    return get_api_info()


@app.get(
    "/v1",
)
def v1():
    return {"hello": "world v1"}


@app.get(
    "/v1/models",
)
def v1():
    return {"hello": "world v1"}