"""empty message

Revision ID: b4613f16a820
Revises: 1199edada625
Create Date: 2019-12-01 14:39:45.811686

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4613f16a820'
down_revision = '1199edada625'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stories', sa.Column('title', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stories', 'title')
    # ### end Alembic commands ###
