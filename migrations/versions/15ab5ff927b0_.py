"""empty message

Revision ID: 15ab5ff927b0
Revises: 9ee166d1a691
Create Date: 2017-12-07 16:04:38.266915

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15ab5ff927b0'
down_revision = '9ee166d1a691'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recipe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipe_name', sa.String(length=255), nullable=True),
    sa.Column('instructions', sa.String(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('of_category', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['of_category'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipe')
    # ### end Alembic commands ###