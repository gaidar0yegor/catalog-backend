from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime

Base = declarative_base()

class ImportSourceType(str, enum.Enum):
    FILE_UPLOAD = "file_upload"
    FTP = "ftp"
    API = "api"
    WEB_SCRAPING = "web_scraping"
    EMAIL = "email"

class ProcessingStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETE = "complete"
    FAILED = "failed"

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    source_type = Column(Enum(ImportSourceType))
    configuration = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    catalogs = relationship("Catalog", back_populates="supplier")

class Catalog(Base):
    __tablename__ = "catalogs"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    file_name = Column(String)
    file_size = Column(Integer)
    file_type = Column(String)
    status = Column(Enum(ProcessingStatus), default=ProcessingStatus.PENDING)
    minio_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)

    supplier = relationship("Supplier", back_populates="catalogs")
    field_mappings = relationship("FieldMapping", back_populates="catalog")

class FieldMapping(Base):
    __tablename__ = "field_mappings"

    id = Column(Integer, primary_key=True, index=True)
    catalog_id = Column(Integer, ForeignKey("catalogs.id"))
    source_field = Column(String)
    target_field = Column(String)
    is_required = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    catalog = relationship("Catalog", back_populates="field_mappings")
