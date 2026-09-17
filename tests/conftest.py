import os
import sys
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

# Deben estar seteadas ANTES del primer import de Config.project_config
# (los valores por defecto de sus campos se leen con os.getenv al definir
# la clase, una sola vez por proceso).
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-do-not-use-in-prod")
os.environ.setdefault("CORS_ORIGINS", "")
os.environ.setdefault("DB_ENGINE", "postgresql")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_USER", "test")
os.environ.setdefault("DB_PASSWORD", "test")
os.environ.setdefault("DB_NAME", "test")

from sqlmodel import SQLModel

from Models.Context.sqlalchemy_context import SqlalchemyContext
from Models.Repository.sqlalchemy_generic_repository import SqlAlchemyGenericRepository

# Importar todos los modelos para que SQLModel.metadata conozca cada tabla
# (y sus foreign keys) antes de crear el esquema de prueba.
from Models.User.user import User
from Models.Roles.rolesTy import RolesTy
from Models.Roles.roles import Roles
from Models.Plantas.plantas_Cat import Plantas_Cat
from Models.Plantas.plantas import Plantas
from Models.Plagas.plagas import Plags
from Models.PlagXPlants.plagxplants import Plagsxplants
from Models.Plantaciones.plantaciones import Plants_mp
from Models.RecordatoriosCuidados.recordCui import RecordCui
from Models.SintomaPlanta.sintoma_planta import Sintoma_Planta
from Models.Token.token_blacklist import Token_blacklist


@pytest.fixture()
def db_context(tmp_path):
    """Una base sqlite nueva y vacía por test, con el esquema completo
    creado directamente desde los modelos (no vía Alembic: sqlite no
    soporta el ALTER TABLE que usan las migraciones reales, ver README de
    /tests)."""
    db_path = tmp_path / "test.db"
    context = SqlalchemyContext(db_url=f"sqlite:///{db_path}")
    SQLModel.metadata.create_all(context._engine)
    return context


@pytest.fixture()
def repo_factory(db_context):
    def _factory(entity):
        return SqlAlchemyGenericRepository(db_context, entity)
    return _factory
