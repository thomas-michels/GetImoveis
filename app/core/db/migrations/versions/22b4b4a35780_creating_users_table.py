"""creating_users_table

Revision ID: 22b4b4a35780
Revises: 3cd8f633cb71
Create Date: 2024-05-26 21:21:24.452926

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22b4b4a35780'
down_revision: Union[str, None] = '3cd8f633cb71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
CREATE TABLE users (
	id serial4 NOT NULL,
	first_name varchar(30) NOT NULL,
	last_name varchar(50) NOT NULL,
	email varchar(50) NOT NULL,
	"password" varchar(100) NOT NULL,
	created_at timestamp with time zone NOT NULL,
	updated_at timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
	CONSTRAINT users_pk PRIMARY KEY (id),
	CONSTRAINT users_un UNIQUE (email)
);
""")


def downgrade() -> None:
    pass
