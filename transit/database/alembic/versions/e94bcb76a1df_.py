"""empty message

Revision ID: e94bcb76a1df
Revises: 
Create Date: 2024-06-04 00:51:31.105886

"""

from typing import Sequence, Union

import sqlmodel

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e94bcb76a1df"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "transit_gateways",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("user_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("vytransit_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "operating_status", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column(
            "provisioning_status", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "transit_gateway_peerings",
        sa.Column(
            "transit_gateway_first_id",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
        ),
        sa.Column(
            "transit_gateway_second_id",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["transit_gateway_first_id"],
            ["transit_gateways.id"],
        ),
        sa.ForeignKeyConstraint(
            ["transit_gateway_second_id"],
            ["transit_gateways.id"],
        ),
        sa.PrimaryKeyConstraint(
            "transit_gateway_first_id", "transit_gateway_second_id"
        ),
    )
    op.create_table(
        "vpcs",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "transit_gateway_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["transit_gateway_id"],
            ["transit_gateways.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "subnets",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("address", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("vpc_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.ForeignKeyConstraint(
            ["vpc_id"],
            ["vpcs.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("subnets")
    op.drop_table("vpcs")
    op.drop_table("transit_gateway_peerings")
    op.drop_table("transit_gateways")
    # ### end Alembic commands ###
