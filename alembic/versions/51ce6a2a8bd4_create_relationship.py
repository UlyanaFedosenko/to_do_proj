"""create relationship

Revision ID: 51ce6a2a8bd4
Revises: 27588433926a
Create Date: 2024-03-22 23:46:53.226999

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51ce6a2a8bd4'
down_revision: Union[str, None] = '27588433926a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_foreign_key('fk_task_user', 'tasks', 'users', ['user_id'], ['id'])


def downgrade():
    op.drop_constraint('fk_task_user', 'tasks', type_='foreignkey')
