from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse, Response

from api.pydantic.models import Pagination
from infrastructure.repositories.postgresql.author import PostgreSQLAuthorRepository

from .models import AuthorSchema, CreateUpdateAuthorSchema

router = APIRouter(prefix='/authors')
