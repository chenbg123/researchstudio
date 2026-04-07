from sqlalchemy.orm import Session

from app.db.models.admin_visibility import AdminVisibility


class VisibilityService:
    def __init__(self, db: Session):
        self.db = db

    def set_rule(self, *, category: str, key: str, enabled: bool) -> AdminVisibility:
        rule = self.db.query(AdminVisibility).filter_by(category=category, key=key).one_or_none()
        if rule is None:
            rule = AdminVisibility(category=category, key=key, enabled=enabled)
            self.db.add(rule)
        else:
            rule.enabled = enabled
        self.db.commit()
        self.db.refresh(rule)
        return rule

    def get_enabled_map(self, category: str) -> dict[str, bool]:
        rules = self.db.query(AdminVisibility).filter_by(category=category).all()
        return {rule.key: rule.enabled for rule in rules}
