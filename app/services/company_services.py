from app.schemas.company import CompanyCreate,CompanyUpdate
from app.errors import NotFoundError
from sqlalchemy.orm import Session
from app.models.company import Company


# returns all companies
def get_all_companies(db:Session, skip:int=0,limit:int=10,sort_by="id")->dict:
    valid_sort_field={"id","name","industry"}

    if sort_by not in valid_sort_field:
        sort_by="id"

    column=getattr(Company,sort_by)
    total=db.query(Company).count()
    companies=db.query(Company).order_by(column).offset(skip).limit(limit).all()

    return {
        "total":total,
        "skip":skip,
        "limit":limit,
        "companies":companies
    }

# return company by id
def get_company_by_id(db:Session,company_id:int)->Company:
    company = db.query(Company).filter(Company.id==company_id).first()
    if not company:
        raise NotFoundError("Company")
    return company

def create_company(db:Session,company_data:CompanyCreate)->Company:
    new_company= Company(**company_data.model_dump())
    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company


def update_company(db:Session,comp_id:int,updates:CompanyUpdate)->Company:
    company=get_company_by_id(db,comp_id)
    update_data = updates.model_dump(exclude_unset=True)
    for field,value in update_data.items():
        setattr(company,field,value)
    db.commit()
    db.refresh(company)
    return company

def delete_company(db:Session,comp_id: int)->None:
    company=get_company_by_id(db,comp_id)
    db.delete(company)
    db.commit()
    
