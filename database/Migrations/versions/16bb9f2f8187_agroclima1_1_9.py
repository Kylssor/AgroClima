"""AgroClima1.1-9

Revision ID: 16bb9f2f8187
Revises: 22336a307038
Create Date: 2026-09-17 00:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16bb9f2f8187'
down_revision: Union[str, None] = '22336a307038'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 'user.roles' y 'roles.user' formaban una FK circular con AMBOS lados
    # NOT NULL desde la migración original: para crear un 'user' hacía
    # falta que ya existiera una fila en 'roles', y para crear una fila en
    # 'roles' hacía falta que ya existiera el 'user' al que apunta — un
    # candado que nunca se pudo abrir. En la práctica esto hacía imposible
    # crear un usuario nuevo (POST /auth/signUp) contra un Postgres real.
    # Se relaja 'user.roles' a NULL: un usuario puede existir sin rol
    # asignado todavía, y un Role se crea después apuntando a un user que
    # ya existe.
    op.alter_column('user', 'roles', existing_type=sa.UUID(), nullable=True)


def downgrade() -> None:
    op.alter_column('user', 'roles', existing_type=sa.UUID(), nullable=False)
