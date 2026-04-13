"""add check and unique constraints for domain validation

Revision ID: 20260413_03
Revises: 20260302_02
Create Date: 2026-04-13
"""

from alembic import op


revision = "20260413_03"
down_revision = "20260302_02"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("survey_responses") as batch_op:
        batch_op.create_check_constraint(
            "ck_survey_responses_user_id_positive",
            "user_id > 0",
        )
        batch_op.create_check_constraint(
            "ck_survey_responses_survey_id_positive",
            "survey_id > 0",
        )
        batch_op.create_check_constraint(
            "ck_survey_responses_department_id_positive",
            "department_id IS NULL OR department_id > 0",
        )
        batch_op.create_check_constraint(
            "ck_survey_responses_overall_score_range",
            "overall_score IS NULL OR (overall_score >= 0 AND overall_score <= 5)",
        )

    with op.batch_alter_table("ai_risk_assessments") as batch_op:
        batch_op.create_check_constraint(
            "ck_ai_risk_assessments_user_id_positive",
            "user_id > 0",
        )
        batch_op.create_check_constraint(
            "ck_ai_risk_assessments_risk_score_range",
            "risk_score >= 0 AND risk_score <= 100",
        )
        batch_op.create_check_constraint(
            "ck_ai_risk_assessments_risk_level_allowed",
            "risk_level IN ('low', 'medium', 'high')",
        )

    with op.batch_alter_table("question_responses") as batch_op:
        batch_op.create_check_constraint(
            "ck_question_responses_answer_value_range",
            "answer_value >= 0 AND answer_value <= 5",
        )
        batch_op.create_unique_constraint(
            "uq_question_responses_response_question",
            ["response_id", "question_id"],
        )

    with op.batch_alter_table("consent_records") as batch_op:
        batch_op.create_check_constraint(
            "ck_consent_records_user_id_positive",
            "user_id > 0",
        )


def downgrade() -> None:
    with op.batch_alter_table("consent_records") as batch_op:
        batch_op.drop_constraint("ck_consent_records_user_id_positive", type_="check")

    with op.batch_alter_table("question_responses") as batch_op:
        batch_op.drop_constraint("uq_question_responses_response_question", type_="unique")
        batch_op.drop_constraint("ck_question_responses_answer_value_range", type_="check")

    with op.batch_alter_table("ai_risk_assessments") as batch_op:
        batch_op.drop_constraint("ck_ai_risk_assessments_risk_level_allowed", type_="check")
        batch_op.drop_constraint("ck_ai_risk_assessments_risk_score_range", type_="check")
        batch_op.drop_constraint("ck_ai_risk_assessments_user_id_positive", type_="check")

    with op.batch_alter_table("survey_responses") as batch_op:
        batch_op.drop_constraint("ck_survey_responses_overall_score_range", type_="check")
        batch_op.drop_constraint("ck_survey_responses_department_id_positive", type_="check")
        batch_op.drop_constraint("ck_survey_responses_survey_id_positive", type_="check")
        batch_op.drop_constraint("ck_survey_responses_user_id_positive", type_="check")
