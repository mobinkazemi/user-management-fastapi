from shared.functions.to_dict import to_dict
from shared.repository.baseRepository import BaseRepository
from . import model


class RoleRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(model.Role)

    def updateOne(self, id, updateData):
        if updateData.get("name", None) and self.duplicate_name_on_update_role(
            id, updateData["name"]
        ):
            return None

        return super().updateOne(id, updateData)

    def duplicate_name_on_update_role(self, id: int, name: str):
        role = self.session.query(self.model).filter(self.model.name == name).first()
        if role:
            return to_dict(role)

        return None
