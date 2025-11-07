from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class VideoAnalysis(Base):
    __tablename__ = "video_analysis"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    violations = relationship(
        "Violation", back_populates="analysis", cascade="all, delete-orphan"
    )


class Violation(Base):
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("video_analysis.id", ondelete="CASCADE"))
    frame = Column(Integer)
    type = Column(String)
    confidence = Column(Float)

    analysis = relationship("VideoAnalysis", back_populates="violations")
