import enum

from sqlalchemy import Column, Enum, Integer, ForeignKey, Text, VARCHAR
from sqlalchemy.orm import relationship, validates

from database import Base


class Status(enum.Enum):
    new = "NEW"
    in_progress = "IN PROGRESS"
    completed = "COMPLETED"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR(20), nullable=False)
    last_name = Column(Text)
    username = Column(VARCHAR(30), unique=True, nullable=False)
    password = Column(VARCHAR(20), nullable=False)

    @validates('password')
    def validate_password(self, key, password):
        if len(password) < 6:
            raise ValueError('The password must be minimum 6 characters long.')
        return password


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(50), nullable=False)
    description = Column(Text)
    status = Column(Enum(Status, name="statuses"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tasks")