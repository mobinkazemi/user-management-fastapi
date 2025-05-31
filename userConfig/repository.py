from shared.functions.to_dict import to_dict
from shared.repository.baseRepository import BaseRepository
from . import model


class UserConfigRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(model.UserConfig)

    def getExpirePasswordDays(self) -> int | None:
        """
        Get the expire password days from the database.
        :return: int | None
        """
        result = (
            self.session.query(self.model)
            .filter(self.model.expirePasswordDays >= 0, self.model.deletedAt == None)
            .first()
        )

        if result is None:
            return 0

        return to_dict(result)["expirePasswordDays"]

    def getPasswordAdvantageDays(self) -> int | None:
        """
        Get the password advantage days from the database.
        :return: int | None
        """
        result = (
            self.session.query(self.model)
            .filter(self.model.passwordAdvantageDays >= 0, self.model.deletedAt == None)
            .first()
        )

        if result is None:
            return 0

        return to_dict(result)["passwordAdvantageDays"]
