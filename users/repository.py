from shared.functions.to_dict import to_dict
from shared.repository.baseRepository import BaseRepository
from . import model


class UserRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(model.User)

    def findByUsername(self, username: str):
        result = (
            self.session.query(self.model)
            .filter(self.model.username == username)
            .first()
        )

        if result is None:
            return None

        return to_dict(result)
