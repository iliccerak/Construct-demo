from sqlalchemy.orm import Session

from infrastructure.persistence import models


def create_company(db: Session, request, owner_user_id: str) -> models.Company:
    company = models.Company(**request.dict())
    db.add(company)
    db.commit()
    db.refresh(company)

    membership = models.CompanyMembership(
        company_id=company.id,
        user_id=owner_user_id,
        role="company_owner",
        is_primary=True,
    )
    db.add(membership)
    db.commit()
    return company


def get_company(db: Session, company_id: str) -> models.Company:
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise ValueError("Company not found")
    return company
