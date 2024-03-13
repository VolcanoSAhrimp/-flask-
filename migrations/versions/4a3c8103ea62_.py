"""empty message

Revision ID: 4a3c8103ea62
Revises: 40471580b50b
Create Date: 2024-03-10 20:32:32.796663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a3c8103ea62'
down_revision = '40471580b50b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('borrow_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('reader_id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('borrow_date', sa.DateTime(), nullable=True),
    sa.Column('return_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['reader_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('borrow_history')
    # ### end Alembic commands ###
