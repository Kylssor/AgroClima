"""AgroClima1.1-7

Revision ID: 14914725563c
Revises: 1073a2a48712
Create Date: 2026-09-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '14914725563c'
down_revision: Union[str, None] = '1073a2a48712'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # RecordatoriosCuidados: pasa de apuntar a un tipo de Planta (catálogo) a
    # apuntar a una Plantacion concreta del usuario, con la info necesaria
    # para calcular recordatorios recurrentes.
    #
    # NOTA: esta migración asume que 'recordcui' está vacía (nunca se
    # expuso service/controller para esa tabla antes de esta versión). Si
    # se aplica sobre un ambiente con filas existentes, 'plantacion_id' no
    # tiene un valor por defecto razonable (no hay forma de mapear una fila
    # vieja, ligada a un tipo de Planta, a una Plantacion concreta de un
    # usuario) y la migración va a fallar por NOT NULL — hay que limpiar o
    # migrar esos datos a mano antes de correrla.
    op.add_column('recordcui', sa.Column('plantacion_id', sqlmodel.sql.sqltypes.GUID(), nullable=False))
    op.add_column('recordcui', sa.Column('tipo_cuidado', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False, server_default='riego'))
    op.add_column('recordcui', sa.Column('frecuencia_dias', sa.Integer(), nullable=False, server_default='1'))
    op.add_column('recordcui', sa.Column('proxima_fecha', sa.DateTime(), nullable=False, server_default=sa.func.now()))
    op.add_column('recordcui', sa.Column('activo', sa.Boolean(), nullable=False, server_default=sa.true()))
    op.alter_column('recordcui', 'tipo_cuidado', server_default=None)
    op.alter_column('recordcui', 'frecuencia_dias', server_default=None)
    op.alter_column('recordcui', 'proxima_fecha', server_default=None)
    op.alter_column('recordcui', 'activo', server_default=None)
    op.create_foreign_key('recordcui_plantacion_id_fkey', 'recordcui', 'plants_mp', ['plantacion_id'], ['id'])
    op.drop_column('recordcui', 'fecha_hora')
    op.drop_column('recordcui', 'record')
    op.drop_column('recordcui', 'Plantas_id')

    # SintomaPlanta: ficha de síntomas/recomendaciones por tipo de Planta.
    op.create_table(
        'sintoma_planta',
        sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('planta_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('sintoma', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column('diagnostico', sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
        sa.Column('recomendacion', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(['planta_id'], ['plantas.id'], name='sintoma_planta_planta_id_fkey'),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('sintoma_planta')

    op.drop_constraint('recordcui_plantacion_id_fkey', 'recordcui', type_='foreignkey')
    op.add_column('recordcui', sa.Column('Plantas_id', sqlmodel.sql.sqltypes.GUID(), nullable=False))
    op.add_column('recordcui', sa.Column('record', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False))
    op.add_column('recordcui', sa.Column('fecha_hora', sa.DateTime(), nullable=False))
    op.create_foreign_key('recordcui_Plantas_id_fkey', 'recordcui', 'plantas', ['Plantas_id'], ['id'])
    op.drop_column('recordcui', 'activo')
    op.drop_column('recordcui', 'proxima_fecha')
    op.drop_column('recordcui', 'frecuencia_dias')
    op.drop_column('recordcui', 'tipo_cuidado')
    op.drop_column('recordcui', 'plantacion_id')
