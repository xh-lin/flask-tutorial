"""followers

Revision ID: 980ad88aabd6
Revises: 22908b6a339b
Create Date: 2020-11-12 11:52:35.675071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '980ad88aabd6'
down_revision = '22908b6a339b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###