"""agroclima1_1_11_fix_plags_recom_column

Revision ID: a642cd723535
Revises: e8d9adf5a163
Create Date: 2026-09-17 23:58:02.385360

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a642cd723535'
down_revision: Union[str, None] = 'e8d9adf5a163'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('plags', 'recomenda', new_column_name='recom')


def downgrade() -> None:
    op.alter_column('plags', 'recom', new_column_name='recomenda')
