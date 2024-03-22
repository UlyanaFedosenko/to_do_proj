"""create tasks table

Revision ID: 27588433926a
Revises: 2dd74653e81c
Create Date: 2024-03-22 16:34:56.599365

"""
import enum

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27588433926a'
down_revision: Union[str, None] = '2dd74653e81c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


class Status(enum.Enum):
    new = "NEW"
    in_progress = "IN PROGRESS"
    completed = "COMPLETED"


def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('title', sa.VARCHAR(50), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('status', sa.Enum(Status, name='statuses'), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'))
    )


def downgrade() -> None:
    op.drop_table('tasks')
