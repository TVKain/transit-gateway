"""empty message

Revision ID: 86423f35660b
Revises: 3f753e990af3
Create Date: 2024-06-24 20:34:42.162317

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import sqlmodel

# revision identifiers, used by Alembic.
revision: str = "86423f35660b"
down_revision: Union[str, None] = "3f753e990af3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "transit_gateway_peering_attachments",
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    op.add_column(
        "transit_gateway_peering_attachments",
        sa.Column("created_at", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    op.add_column(
        "transit_gateway_peering_attachments",
        sa.Column("updated_at", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    op.add_column(
        "transit_gateway_peering_routes",
        sa.Column("status", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    op.add_column(
        "transit_gateway_peering_routes",
        sa.Column("created_at", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    op.add_column(
        "transit_gateway_peering_routes",
        sa.Column("updated_at", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    op.add_column(
        "transit_gateway_vpc_attachments",
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("transit_gateway_vpc_attachments", "name")
    op.drop_column("transit_gateway_peering_routes", "updated_at")
    op.drop_column("transit_gateway_peering_routes", "created_at")
    op.drop_column("transit_gateway_peering_routes", "status")
    op.drop_column("transit_gateway_peering_attachments", "updated_at")
    op.drop_column("transit_gateway_peering_attachments", "created_at")
    op.drop_column("transit_gateway_peering_attachments", "name")
    # ### end Alembic commands ###
