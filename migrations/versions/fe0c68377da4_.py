"""empty message

Revision ID: fe0c68377da4
Revises: 77a38f8a6435
Create Date: 2024-05-18 03:21:34.692162

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe0c68377da4'
down_revision = '77a38f8a6435'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ad', schema=None) as batch_op:
        batch_op.drop_column('rankid')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ad', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rankid', sa.INTEGER(), nullable=True))

    # ### end Alembic commands ###
