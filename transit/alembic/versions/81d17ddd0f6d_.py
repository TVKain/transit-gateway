"""empty message

Revision ID: 81d17ddd0f6d
Revises: 12e9b13b9db7
Create Date: 2024-06-20 08:21:37.104216

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import sqlmodel

# revision identifiers, used by Alembic.
revision: str = "81d17ddd0f6d"
down_revision: Union[str, None] = "12e9b13b9db7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
