"""empty message

Revision ID: 246605450015
Revises: f4813456b443
Create Date: 2024-06-21 02:09:46.776841

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import sqlmodel

# revision identifiers, used by Alembic.
revision: str = "246605450015"
down_revision: Union[str, None] = "f4813456b443"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "transit_gateway_vpc_attachments",
        sa.Column(
            "transit_gateway_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
    )
    op.create_foreign_key(
        None,
        "transit_gateway_vpc_attachments",
        "transit_gateways",
        ["transit_gateway_id"],
        ["id"],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "transit_gateway_vpc_attachments", type_="foreignkey")
    op.drop_column("transit_gateway_vpc_attachments", "transit_gateway_id")
    # ### end Alembic commands ###
