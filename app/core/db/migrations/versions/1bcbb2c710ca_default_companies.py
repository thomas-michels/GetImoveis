"""default-companies

Revision ID: 1bcbb2c710ca
Revises: 873ef9b26213
Create Date: 2023-08-13 20:37:44.779763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bcbb2c710ca'
down_revision: Union[str, None] = '873ef9b26213'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = '873ef9b26213'


def upgrade() -> None:
    op.execute(f"""
INSERT INTO companies("name") VALUES('portal_imoveis');
INSERT INTO companies("name") VALUES('zap_imoveis');
               """)


def downgrade() -> None:
    pass
