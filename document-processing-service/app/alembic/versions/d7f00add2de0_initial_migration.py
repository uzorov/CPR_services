"""Initial migration

Revision ID: d7f00add2de0
Revises: 
Create Date: 2024-08-06 13:09:21.211094

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = 'd7f00add2de0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('documents',
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('file_id', sa.String, nullable=True),
    sa.Column('title', sa.String, nullable=True),
    sa.Column('body', sa.String, nullable=True),
    sa.Column('author_id', UUID(as_uuid=True), nullable=True),
    sa.Column('responsible_employee_id', UUID(as_uuid=True), nullable=True),
    sa.Column('created_at', sa.DateTime, default=sa.func.now(), nullable=True)
    )

def downgrade() -> None:
    op.drop_table('documents')
