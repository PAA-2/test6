from typing import Any, Dict

from sqlalchemy.orm import Session

from app.models.project import Project, ProjectAudit


def create_project(db: Session, *, project_in: Dict[str, Any], user_id: int) -> Project:
    project = Project(**project_in, owner_id=user_id)
    db.add(project)
    db.commit()
    db.refresh(project)
    audit = ProjectAudit(
        project_id=project.id, action="create", actor_id=user_id, diff=None
    )
    db.add(audit)
    db.commit()
    return project


def update_project(
    db: Session, *, project: Project, data: Dict[str, Any], user_id: int
) -> Project:
    before = {c.name: getattr(project, c.name) for c in project.__table__.columns}
    for field, value in data.items():
        setattr(project, field, value)
    db.add(project)
    db.commit()
    db.refresh(project)
    after = {c.name: getattr(project, c.name) for c in project.__table__.columns}

    def serialize(d: Dict[str, Any]) -> Dict[str, str]:
        return {k: str(v) for k, v in d.items()}

    diff = {"before": serialize(before), "after": serialize(after)}
    db.add(
        ProjectAudit(
            project_id=project.id, action="update", actor_id=user_id, diff=diff
        )
    )
    db.commit()
    return project


def delete_project(db: Session, *, project: Project, user_id: int) -> None:
    db.delete(project)
    db.commit()
    db.add(
        ProjectAudit(
            project_id=project.id, action="delete", actor_id=user_id, diff=None
        )
    )
    db.commit()
