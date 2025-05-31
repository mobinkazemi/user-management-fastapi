from shared.repository.baseRepository import BaseRepository
from . import model
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from permissionsCategory.model import PermissionCategory


class PermissionRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(model.Permission)

    def get_all_permissions_grouped_with_category(self):

        stmt = select(PermissionCategory).options(
            selectinload(PermissionCategory.permissions)
        )

        categories = self.session.execute(stmt).scalars().all()

        result = [r.__dict__ for r in categories]

        for r in result:
            r.pop("_sa_instance_state", None)
            r["permissions"] = [p.__dict__ for p in r["permissions"]]
            for p in r["permissions"]:
                p.pop("_sa_instance_state", None)
                p.pop("category_id", None)

        return result

    def get_filtered_permissions_grouped_with_category(self, category_id: int):

        stmt = (
            select(PermissionCategory)
            .options(selectinload(PermissionCategory.permissions))
            .where(PermissionCategory.id == category_id)
        )

        categories = self.session.execute(stmt).scalars().all()

        result = [r.__dict__ for r in categories]

        for r in result:
            r.pop("_sa_instance_state", None)
            r["permissions"] = [p.__dict__ for p in r["permissions"]]
            for p in r["permissions"]:
                p.pop("_sa_instance_state", None)
                p.pop("category_id", None)

        return result
