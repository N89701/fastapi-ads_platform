"""init

Revision ID: ab23b782d389
Revises: 
Create Date: 2023-11-25 22:50:05.249178

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab23b782d389'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('contact', sa.String(), nullable=False),
    sa.Column('registered_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('advertisement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('pub_date', sa.TIMESTAMP(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_advertisement_id'), 'advertisement', ['id'], unique=False)
    op.create_table('complaint',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('advertisement_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['advertisement_id'], ['advertisement.id'], ),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('photo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('advertisement_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['advertisement_id'], ['advertisement.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_photo_id'), 'photo', ['id'], unique=False)
    op.create_table('recalls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('advertisement_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['advertisement_id'], ['advertisement.id'], ),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recalls')
    op.drop_index(op.f('ix_photo_id'), table_name='photo')
    op.drop_table('photo')
    op.drop_table('complaint')
    op.drop_index(op.f('ix_advertisement_id'), table_name='advertisement')
    op.drop_table('advertisement')
    op.drop_table('group')
    op.drop_table('user')
    op.drop_table('category')
    # ### end Alembic commands ###