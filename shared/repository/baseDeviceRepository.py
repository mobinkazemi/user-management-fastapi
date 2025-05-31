from sqlalchemy import select
from sqlalchemy.orm import Session
from db.database import session
from shared.functions.to_dict import to_dict
from shared.repository.baseRepository import BaseRepository


class BaseNetworkDeviceRepository(BaseRepository):
    def __init__(self, model) -> None:
        self.model = model
        self.session: Session = session

    def findByIP(self, ip: str):
        result = (
            self.session.query(self.model)
            .filter(self.model.ip == ip, self.model.deletedAt == None)
            .first()
        )

        if result is None:
            return None

        return to_dict(result)
