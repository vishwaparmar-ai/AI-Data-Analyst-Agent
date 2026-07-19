from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,JSON
from sqlalchemy.sql import func
from backend.database.database import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    total_rows = Column(Integer)
    total_columns = Column(Integer)
    dataset_metadata = Column(JSON)
    dataset_type = Column(String)
    cleaned_filepath = Column(String)
    cleaning_summary = Column(JSON)
    business_summary = Column(JSON)
    uploaded_at = Column(
    DateTime(timezone=True),
    server_default=func.now()
)