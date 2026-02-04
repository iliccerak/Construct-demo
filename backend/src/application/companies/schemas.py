from pydantic import BaseModel, EmailStr


class CompanyCreateRequest(BaseModel):
    legal_name: str
    trading_name: str | None = None
    registration_number: str | None = None
    tax_id: str | None = None
    vat_number: str | None = None
    currency_code: str = "EUR"
    billing_email: EmailStr | None = None
    phone_number: str | None = None
    website: str | None = None
    address_line_1: str | None = None
    address_line_2: str | None = None
    city: str | None = None
    state_region: str | None = None
    postal_code: str | None = None
    country_code: str = "DE"


class CompanyResponse(BaseModel):
    id: str
    legal_name: str
    trading_name: str | None

    class Config:
        from_attributes = True
