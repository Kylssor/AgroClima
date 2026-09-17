"""AgroClima1.1-8

Revision ID: 22336a307038
Revises: 14914725563c
Create Date: 2026-09-17 00:10:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '22336a307038'
down_revision: Union[str, None] = '14914725563c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # El email solo se validaba como único desde la aplicación
    # (Authentication_service.sign_up), sin respaldo a nivel de base de
    # datos: dos signups concurrentes con el mismo correo podían crear dos
    # cuentas. Si ya existieran duplicados en la tabla 'user', este
    # constraint va a fallar y hay que limpiarlos a mano antes de aplicarlo.
    op.create_unique_constraint('user_email_key', 'user', ['email'])


def downgrade() -> None:
    op.drop_constraint('user_email_key', 'user', type_='unique')
