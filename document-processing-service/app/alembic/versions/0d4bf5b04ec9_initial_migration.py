"""Initial migration

Revision ID: 0d4bf5b04ec9
Revises: 
Create Date: 2024-05-20 22:00:26.956779

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import ARRAY

# revision identifiers, used by Alembic.
revision: str = '0d4bf5b04ec9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create tables
    op.create_table(
        'roles',
        Column('id', Integer, primary_key=True),
        Column('role_code', String),
        Column('role_name', String)
    )
    op.create_table(
        'users',
        Column('id', Integer, primary_key=True),
        Column('full_name', String),
        Column('department', String),
        Column('organization', String),
        Column('password', String),
        Column('role_id', Integer, ForeignKey('roles.id'))
    )

    op.create_table(
        'files',
        Column('id', Integer, primary_key=True),
        Column('file_name', String),
        Column('format', String),
        Column('user_id', Integer, ForeignKey('users.id')),
        Column('created_at', DateTime, default=datetime.utcnow)
    )
    op.create_table(
        'documents',
        Column('id', Integer, primary_key=True),
        Column('file_ids', ARRAY(Integer)),
        Column('title', String),
        Column('body', String),
        Column('author_id', Integer, ForeignKey('users.id')),
        Column('responsible_employee_id', Integer, ForeignKey('users.id')),
        Column('created_at', DateTime, default=datetime.utcnow)
    )



def downgrade() -> None:
    # Drop tables
    op.drop_table('documents')
    op.drop_table('files')
    op.drop_table('roles')
    op.drop_table('users')

