"""empty message

Revision ID: 3c55819ffc5b
Revises: 
Create Date: 2024-06-20 07:01:36.364864

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import sqlmodel

# revision identifiers, used by Alembic.
revision: str = "3c55819ffc5b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "transit_gateways",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("user_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("compute_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("status", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("management_ip", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("vpc_net_ip", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("vpc_net_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("peering_net_ip", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("created_at", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("updated_at", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("transit_gateways")
    # ### end Alembic commands ###
