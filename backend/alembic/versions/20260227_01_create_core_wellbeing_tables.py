"""create core wellbeing tables

Revision ID: 20260227_01
Revises:
Create Date: 2026-02-27
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260227_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "survey_responses",
        sa.Column("response_id", sa.Integer(), primary_key=True),
        sa.Column("survey_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("overall_score", sa.Float(), nullable=True),
    )
    op.create_index("ix_survey_responses_survey_id", "survey_responses", ["survey_id"])
    op.create_index("ix_survey_responses_user_id", "survey_responses", ["user_id"])

    op.create_table(
        "ai_risk_assessments",
        sa.Column("assessment_id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("risk_level", sa.String(length=50), nullable=False),
        sa.Column("risk_score", sa.Float(), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_ai_risk_assessments_user_id", "ai_risk_assessments", ["user_id"])

    op.create_table(
        "question_responses",
        sa.Column("question_response_id", sa.Integer(), primary_key=True),
        sa.Column("response_id", sa.Integer(), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("answer_value", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["response_id"], ["survey_responses.response_id"], ondelete="CASCADE"),
    )
    op.create_index("ix_question_responses_response_id", "question_responses", ["response_id"])
    op.create_index("ix_question_responses_question_id", "question_responses", ["question_id"])

    op.create_table(
        "recommendations",
        sa.Column("recommendation_id", sa.Integer(), primary_key=True),
        sa.Column("assessment_id", sa.Integer(), nullable=False),
        sa.Column("recommendation_text", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["assessment_id"], ["ai_risk_assessments.assessment_id"], ondelete="CASCADE"),
    )
    op.create_index("ix_recommendations_assessment_id", "recommendations", ["assessment_id"])


def downgrade() -> None:
    op.drop_index("ix_recommendations_assessment_id", table_name="recommendations")
    op.drop_table("recommendations")

    op.drop_index("ix_question_responses_question_id", table_name="question_responses")
    op.drop_index("ix_question_responses_response_id", table_name="question_responses")
    op.drop_table("question_responses")

    op.drop_index("ix_ai_risk_assessments_user_id", table_name="ai_risk_assessments")
    op.drop_table("ai_risk_assessments")

    op.drop_index("ix_survey_responses_user_id", table_name="survey_responses")
    op.drop_index("ix_survey_responses_survey_id", table_name="survey_responses")
    op.drop_table("survey_responses")
