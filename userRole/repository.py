from shared.functions.to_dict import to_dict
from shared.repository.baseRepository import BaseRepository
from . import model


class UserRoleRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(model.UserRole)
