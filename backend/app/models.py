from pydantic import BaseModel, Field
from typing import Optional

class Report(BaseModel):
    report_date: str
    country: str
    region: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    confirmed_cases: int = 0
    deaths: Optional[int] = None
    virus_type: Optional[str] = None
    source_name: str
    source_url: str
    notes: Optional[str] = None

class LiveItem(BaseModel):
    id: Optional[int] = None
    title: str
    source_name: str
    source_url: str
    published_at: Optional[str] = None
    summary: Optional[str] = None
    matched_keywords: list[str] = Field(default_factory=list)
    created_at: Optional[str] = None
