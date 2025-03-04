"""create summaries table

Revision ID: xxxx
Revises: 12719228d0d9
Create Date: 2024-xx-xx

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "xxxx"  # This will be auto-generated
down_revision = "12719228d0d9"  # Your previous migration
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "summaries",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("summary_text", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("date_summarized", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("summaries")
