"""empty message

Revision ID: b9468de31a7a
Revises: 
Create Date: 2023-09-11 23:12:42.538336

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9468de31a7a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('option',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=255), nullable=False),
    sa.Column('is_correct', sa.Boolean(), nullable=True),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('option')
    op.drop_table('question')
    # ### end Alembic commands ###
