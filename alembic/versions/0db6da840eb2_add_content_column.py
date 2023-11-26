"""add content column

Revision ID: 0db6da840eb2
Revises: 86736362d7fd
Create Date: 2023-11-20 21:43:22.864398

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0db6da840eb2'
down_revision: Union[str, None] = '86736362d7fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass