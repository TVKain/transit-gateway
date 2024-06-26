"""empty message

Revision ID: 20f3e0da8369
Revises: 28580854324a
Create Date: 2024-06-22 00:23:16.694935

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

import sqlmodel

# revision identifiers, used by Alembic.
revision: str = "20f3e0da8369"
down_revision: Union[str, None] = "28580854324a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "vpc_transit_gateway_routes",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("vpc_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("target", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("destination", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("created_at", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("updated_at", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.ForeignKeyConstraint(
            ["target"],
            ["transit_gateway_vpc_attachments.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_table("vpc_transit_routes")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "vpc_transit_routes",
        sa.Column("id", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("target", mysql.VARCHAR(length=255), nullable=True),
        sa.Column("destination", mysql.VARCHAR(length=255), nullable=True),
        sa.Column("created_at", mysql.VARCHAR(length=255), nullable=True),
        sa.Column("updated_at", mysql.VARCHAR(length=255), nullable=True),
        sa.ForeignKeyConstraint(
            ["target"],
            ["transit_gateway_vpc_attachments.id"],
            name="vpc_transit_routes_ibfk_1",
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_collate="utf8mb3_general_ci",
        mysql_default_charset="utf8mb3",
        mysql_engine="InnoDB",
    )
    op.drop_table("vpc_transit_gateway_routes")
    # ### end Alembic commands ###
