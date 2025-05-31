from shared.repository.baseRepository import BaseRepository
from . import model


class PermissionCategoryRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(model.PermissionCategory)
