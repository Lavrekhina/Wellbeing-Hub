"""add department mapping and consent records

Revision ID: 20260302_02
Revises: 20260227_01
Create Date: 2026-03-02
"""

from alembic import op
import sqlalchemy as sa


revision = "20260302_02"
down_revision = "20260227_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("survey_responses", sa.Column("department_id", sa.Integer(), nullable=True))
    op.create_index("ix_survey_responses_department_id", "survey_responses", ["department_id"])

    op.create_table(
        "consent_records",
        sa.Column("consent_id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("consent_type", sa.String(length=50), nullable=False),
        sa.Column("granted", sa.Boolean(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_consent_records_user_id", "consent_records", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_consent_records_user_id", table_name="consent_records")
    op.drop_table("consent_records")

    op.drop_index("ix_survey_responses_department_id", table_name="survey_responses")
    op.drop_column("survey_responses", "department_id")
