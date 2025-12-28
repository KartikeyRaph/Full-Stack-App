from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    status: str = Field(default="idea")  # idea, active, completed, archived
    priority: int = Field(default=2)
    created_at: datetime = Field(default_factory=datetime.utcnow)
