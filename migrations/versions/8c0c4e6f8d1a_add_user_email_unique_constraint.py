"""Add the user email uniqueness constraint.

Revision ID: 8c0c4e6f8d1a
Revises: 5ae0df790903
"""
from alembic import op
import sqlalchemy as sa


revision = "8c0c4e6f8d1a"
down_revision = "5ae0df790903"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user") as batch_op:
        batch_op.create_unique_constraint("uq_user_email", ["email"])


def downgrade():
    with op.batch_alter_table("user") as batch_op:
        batch_op.drop_constraint("uq_user_email", type_="unique")
