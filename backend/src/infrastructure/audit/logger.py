from sqlalchemy.orm import Session

from infrastructure.persistence.models import AuditLog


def log_event(
    db: Session,
    action: str,
    entity_type: str,
    entity_id: str | None,
    actor_user_id: str | None,
    company_id: str | None,
    ip_address: str | None,
    user_agent: str | None,
    metadata: dict | None = None,
) -> None:
    record = AuditLog(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        actor_user_id=actor_user_id,
        company_id=company_id,
        ip_address=ip_address,
        user_agent=user_agent,
        metadata=metadata or {},
    )
    db.add(record)
    db.commit()
