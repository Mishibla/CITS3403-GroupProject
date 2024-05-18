"""empty message

Revision ID: 1cd7919f6d2c
Revises: 830e5e21c19c
Create Date: 2024-05-17 04:08:16.215528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cd7919f6d2c'
down_revision = '830e5e21c19c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_user')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('phone', sa.String(length=100), nullable=True))
        batch_op.alter_column('wishlist',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.Integer(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('wishlist',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
        batch_op.drop_column('phone')
        batch_op.drop_column('email')

    op.create_table('_alembic_tmp_user',
    sa.Column('username', sa.VARCHAR(length=100), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('password_hash', sa.VARCHAR(length=100), nullable=False),
    sa.Column('wishlist', sa.INTEGER(), nullable=True),
    sa.Column('email', sa.VARCHAR(length=100), nullable=False),
    sa.Column('phone', sa.VARCHAR(length=100), nullable=True),
    sa.PrimaryKeyConstraint('username')
    )
    # ### end Alembic commands ###
