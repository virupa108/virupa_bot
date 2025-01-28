"""add integer primary key

Revision ID: 12719228d0d9
Revises: previous_revision_id
Create Date: 2024-xx-xx

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12719228d0d9'
down_revision: Union[str, None] = '679ed7aa0809'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add tweet_id column allowing nulls initially
    op.add_column('tweets', sa.Column('tweet_id', sa.String(), nullable=True))

    # 2. Copy data from id to tweet_id
    op.execute('UPDATE tweets SET tweet_id = id::varchar')

    # 3. Make tweet_id not null
    op.alter_column('tweets', 'tweet_id',
                    existing_type=sa.String(),
                    nullable=False)

    # 4. Add index and unique constraint
    op.create_index('ix_tweets_tweet_id', 'tweets', ['tweet_id'])
    op.create_unique_constraint('uq_tweets_tweet_id', 'tweets', ['tweet_id'])

    # 5. Create new id column as BIGSERIAL (auto-incrementing BIGINT)
    op.execute('ALTER TABLE tweets DROP CONSTRAINT tweets_pkey')
    op.execute('ALTER TABLE tweets ADD COLUMN new_id BIGSERIAL PRIMARY KEY')
    op.execute('ALTER TABLE tweets DROP COLUMN id')
    op.execute('ALTER TABLE tweets RENAME COLUMN new_id TO id')


def downgrade() -> None:
    # Remove constraints and index
    op.drop_constraint('uq_tweets_tweet_id', 'tweets', type_='unique')
    op.drop_index('ix_tweets_tweet_id', table_name='tweets')

    # Change id back to string
    op.execute('ALTER TABLE tweets DROP CONSTRAINT tweets_pkey')
    op.execute('ALTER TABLE tweets ALTER COLUMN id TYPE varchar')
    op.execute('ALTER TABLE tweets ADD PRIMARY KEY (id)')

    # Drop tweet_id column
    op.drop_column('tweets', 'tweet_id')
