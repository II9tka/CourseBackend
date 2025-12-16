from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from infrastructure.databases.postgresql.session_manager import DatabaseSessionManager
from infrastructure.repositories.postgresql.author import PostgreSQLAuthorUnitOfWork
from infrastructure.repositories.postgresql.user import PostgreSQLUserUnitOfWork

class Container(DeclarativeContainer):
    session_manager = Singleton(DatabaseSessionManager)

    author_uow_factory = Factory(PostgreSQLAuthorUnitOfWork)
    user_uow_factory = Factory(PostgreSQLUserUnitOfWork)