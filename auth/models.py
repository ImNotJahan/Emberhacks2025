from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class UserDto:
    username: str
    email: str
    password: str

@dataclass
class User:
    id: Optional[int]
    username: str
    email: str
    password: str

    @staticmethod
    def from_dto(dto: UserDto):
        return User(None, dto.username, dto.email, dto.password)

    @classmethod
    def from_record(cls, record: tuple):
        if len(record) == 4:
            return cls(id=record[0], username=record[1], email=record[2], password=record[3])
        raise ValueError(f"Record tuple must contain 4 elements: id, username, email, password. Got {len(record)}")

@dataclass
class RequestDto:
    author_id: int
    req: str
    value: float
    solution: str
    equation: str

@dataclass
class RequestDtoResponse:
    id: int
    req: str
    value: float
    solution: str
    equation: str
    timestamp: datetime

@dataclass
class Request:
    id: Optional[int]
    author_id: int
    req: str
    value: float
    solution: str
    equation: str
    timestamp: datetime

    @staticmethod
    def from_dto(dto: RequestDto):
        return Request(None, dto.author_id, dto.req,
                       dto.value, dto.solution,dto.equation, datetime.now())

    def to_dto(self) -> RequestDtoResponse:
        return RequestDtoResponse(self.id, self.req,
                                  self.value, self.solution, self.equation,
                                  self.timestamp)

    @classmethod
    def from_record(cls, record: tuple):
        if len(record) == 7:
            return cls(id=record[0], author_id=record[1], req=record[2],
                       value=record[3], solution=record[4], equation=record[5],
                       timestamp=record[6])
        raise ValueError(f"Record tuple must contain 7 elements. Got {len(record)}")