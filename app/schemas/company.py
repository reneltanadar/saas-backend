from pydantic import BaseModel,field_validator
from typing import Optional
from datetime import datetime

class CompanyCreate(BaseModel):
    name:str
    industry:Optional[str]=None

    @field_validator("name")
    @classmethod
    def emptyname(cls,v):
        if not v.strip():
            raise ValueError("Company Name Cannot Be Empty")
        return v.strip()
    
class CompanyUpdate(BaseModel):
    name:Optional[str]=None
    industry:Optional[str]=None

class CompanyResponse(BaseModel):
    id:int
    name:str
    industry:Optional[str]=None
    created_at:datetime

    model_config ={"from_attributes": True}

class PaginatedCompanies(BaseModel):
    total:int
    skip:int
    limit:int
    companies:list[CompanyResponse]