"""auto_migration

Revision ID: 9a2a203b7154
Revises: fd632e3d3567
Create Date: 2025-03-30 04:45:19.207763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a2a203b7154'
down_revision: Union[str, None] = 'fd632e3d3567'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sensores')
    op.drop_table('nodos_sensores')
    op.drop_table('iot_gateways')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('iot_gateways',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
    sa.Column('associated_mine', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('brand', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='iot_gateways_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('nodos_sensores',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('brand', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('zone_category', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('zone_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('id_iot_gateway', sa.UUID(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_iot_gateway'], ['iot_gateways.id'], name='nodos_sensores_id_iot_gateway_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='nodos_sensores_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('sensores',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
    sa.Column('id_node', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('variable', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('marca', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('referencia', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('unidad_medicion', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('max_medicion', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('min_medicion', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('precision', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('tiempo_respuesta_valor', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('tiempo_respuesta_unidad', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('resolucion', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('temperatura_max', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('temperatura_min', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('voltaje_tipo', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('voltaje_min', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('voltaje_max', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('corriente_min', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('corriente_max', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('durabilidad_valor', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('durabilidad_unidad', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('modo_instalacion', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('tipo_salida', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('certificados', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_node'], ['nodos_sensores.id'], name='sensores_id_node_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='sensores_pkey')
    )
    # ### end Alembic commands ###
