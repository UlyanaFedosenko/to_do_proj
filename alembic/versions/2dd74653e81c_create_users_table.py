"""create users table

Revision ID: 2dd74653e81c
Revises: 
Create Date: 2024-03-22 16:34:09.248582

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2dd74653e81c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('first_name', sa.VARCHAR(20), nullable=False),
        sa.Column('last_name', sa.Text),
        sa.Column('user_name', sa.VARCHAR(30), unique=True),
        sa.Column('password', sa.VARCHAR(20), nullable=False)
    )

    op.execute('''
            CREATE OR REPLACE FUNCTION validate_password() RETURNS TRIGGER AS $$
            BEGIN
                IF LENGTH(NEW.password) < 6 THEN
                    RAISE EXCEPTION 'The password must be minimum 6 characters long.';
                END IF;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER validate_password_trigger
            BEFORE INSERT OR UPDATE ON users
            FOR EACH ROW
            EXECUTE FUNCTION validate_password();
        ''')


def downgrade() -> None:
    op.execute('DROP TRIGGER IF EXISTS validate_password_trigger ON users;')
    op.execute('DROP FUNCTION IF EXISTS validate_password;')
    op.drop_table('users')
