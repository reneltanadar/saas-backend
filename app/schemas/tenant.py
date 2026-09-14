from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class TenantCreate(BaseModel):
    name: str
    slug: str

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Tenant name cannot be empty")
        return v.strip()

    @field_validator("slug")
    @classmethod
    def slug_format(cls, v):
        import re
        if not re.match(r'^[a-z0-9-]+$', v):
            raise ValueError("Slug must be lowercase letters, numbers and hyphens only")
        return v


class TenantUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None


class TenantResponse(BaseModel):
    id: int
    name: str
    slug: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}