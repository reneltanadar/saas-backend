from fastapi import HTTPException
from app.schemas.company import CompanyCreate,CompanyUpdate

companies=[]
counter=1

# returns all companies
def get_all_companies():
    return companies

# return company by id
def get_company_by_id(company_id:int):
    for company in companies:
        if company["id"]==company_id:
            return company
    
    raise HTTPException(
        status_code=404,
        detail="Company Not Found"
    )

def create_company(company_data:CompanyCreate):
    global counter
    
    new_company={
        "id":counter,
        **company_data.model_dump()
    }

    counter+=1
    companies.append(new_company)
    return new_company


def update_company(comp_id:int,updates:CompanyUpdate):
    company=get_company_by_id(comp_id)
    update_data = updates.model_dump(exclude_unset=True)

    company.update(update_data)
    return company

def delete_company(comp_id: int):
    company=get_company_by_id(comp_id)

    companies.remove(company)
    
