from sqlalchemy import Column, DateTime, Integer, func


class BaseDBModel:
    parentId = Column(Integer, nullable=True)
    order = Column(Integer, nullable=True)
    createdAt = Column(DateTime, nullable=False, default=func.now())
    updatedAt = Column(
        DateTime,
        nullable=True,
    )
    deletedAt = Column(DateTime, nullable=True)
