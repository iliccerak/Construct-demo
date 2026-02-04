from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from application.companies.schemas import CompanyCreateRequest
from application.companies.service import create_company, get_company
from application.auth.rbac import has_permission
from presentation.api.v1.dependencies import get_current_user, get_db, require_company_scope

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("")
def create(request: CompanyCreateRequest, user_payload=Depends(get_current_user), db: Session = Depends(get_db)):
    user, payload = user_payload
    role = payload.get("role", "worker")
    if not has_permission(role, "company.create"):
        raise HTTPException(status_code=403, detail="Forbidden")
    company = create_company(db, request, str(user.id))
    return {"id": str(company.id), "legal_name": company.legal_name}


@router.get("/{company_id}")
def get(company_id: str, user_payload=Depends(require_company_scope), db: Session = Depends(get_db)):
    try:
        company = get_company(db, company_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {
        "id": str(company.id),
        "legal_name": company.legal_name,
        "trading_name": company.trading_name,
        "currency_code": company.currency_code,
    }
