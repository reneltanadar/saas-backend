from pydantic import BaseModel,field_validator
from typing import Optional

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

class PaginatedCompanies(BaseModel):
    total:int
    skip:int
    limit:int
    companies:list[CompanyResponse]