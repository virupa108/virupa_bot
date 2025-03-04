"""

Revision ID: 429dce546f89
Revises: 97c7c7fee63e
Create Date: 2025-02-13 15:21:18.257687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '429dce546f89'
down_revision: Union[str, None] = '97c7c7fee63e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tweets', 'llm_response')
    op.drop_column('tweets', 'processed_by_llm')
    op.drop_column('tweets', 'metrics')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tweets', sa.Column('metrics', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.add_column('tweets', sa.Column('processed_by_llm', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('tweets', sa.Column('llm_response', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
