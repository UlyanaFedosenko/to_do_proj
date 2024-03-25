import enum

from sqlalchemy import Column, Enum, Integer, ForeignKey, Text, VARCHAR
from sqlalchemy.orm import relationship, validates

from db.database import Base


class Status(enum.Enum):
    new = "NEW"
    in_progress = "IN PROGRESS"
    completed = "COMPLETED"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR(20), nullable=False)
    last_name = Column(Text)
    user_name = Column(VARCHAR(30), unique=True, nullable=False)
    password = Column(VARCHAR(20), nullable=False)

    def __init__(self, first_name, last_name, user_name, password):
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.password = password

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

    user = relationship("User", backref="tasks")

    def __init__(self, title, description, status, user_id):
        self.title = title
        self.description = description
        self.status = status
        self.user_id = user_id

