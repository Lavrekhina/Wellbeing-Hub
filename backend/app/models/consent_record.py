from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class ConsentRecord(Base):
    __tablename__ = "consent_records"

    __table_args__ = (
        CheckConstraint("user_id > 0", name="ck_consent_records_user_id_positive"),
    )

    consent_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    consent_type: Mapped[str] = mapped_column(String(50), nullable=False, default="survey_checkin")
    granted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
