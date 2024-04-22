"""init Document model

Revision ID: 2eee0e694b57
Revises: 0253786ec574
Create Date: 2024-04-22 21:06:59.271166

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2eee0e694b57"
down_revision: Union[str, None] = "0253786ec574"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
