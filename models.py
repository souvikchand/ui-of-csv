from pydantic import BaseModel
from typing import Optional
from datetime import time


class MetaModel(BaseModel):
    timestamp: str

class DataModel(BaseModel):
    term_code: str
    course_code: str
    seek_course_namespace: Optional[str] = None
    link_to_seek: Optional[str] = None
    program_type: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    exam_date: Optional[str] = None
    level: Optional[str] = None

class RecordModel(BaseModel):
    meta: MetaModel
    data: DataModel