"""empty message

Revision ID: 930d740200fd
Revises: 
Create Date: 2020-07-27 21:04:55.237444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '930d740200fd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assetClass',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('portfolio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('region',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('security',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('region_id', sa.Integer(), nullable=False),
    sa.Column('asset_class_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['asset_class_id'], ['assetClass.id'], ),
    sa.ForeignKeyConstraint(['region_id'], ['region.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('portfolio_composition',
    sa.Column('portfolio_id', sa.Integer(), nullable=False),
    sa.Column('security_id', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['portfolio_id'], ['portfolio.id'], ),
    sa.ForeignKeyConstraint(['security_id'], ['security.id'], ),
    sa.PrimaryKeyConstraint('portfolio_id', 'security_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('portfolio_composition')
    op.drop_table('security')
    op.drop_table('region')
    op.drop_table('portfolio')
    op.drop_table('assetClass')
    # ### end Alembic commands ###