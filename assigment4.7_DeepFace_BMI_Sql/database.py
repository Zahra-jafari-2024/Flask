from sqlmodel import SQLModel, create_engine, Field, Session, select
from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


def relative_time_from_string(time_string):
    parsed_time = datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S')
    current_time = datetime.now()
    time_difference = current_time - parsed_time
    seconds = time_difference.total_seconds()
    if seconds < 60:
        return f"{int(seconds)} seconds ago"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} minutes ago"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} hours ago"
    else:
        days = int(seconds // 86400)
        return f"{days} days ago"

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field()
    password: str = Field()
    firstname: str = Field()
    lastname: str = Field()
    country: str = Field()
    city: str = Field()
    email: str = Field()
    age:int = Field()
    join_time: str = Field()
    comments: List["Comment"] = Relationship(back_populates="user")

class Comment(SQLModel, table=True):
    __table_args__ = {"extend_existing":True}
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    timestamp: datetime = Field(default_factory=datetime.now) 
    services: str
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="comments")


engine = create_engine('postgresql://root:5Jthn9l9aZv6VwB30uIQEg98@thirsty-borg-9tawfy-ii-db:5432/postgres', echo=True)
#engine = create_engine('postgresql://db_user:1234@localhost:15432/db', echo=True)

SQLModel.metadata.create_all(engine)


class RegisterModel(BaseModel):
    username: str
    password: str
    confirm_password: str
    firstname: str
    lastname: str
    country: str
    city: str
    email: str
    age: int
    join_time : str

class LoginModel(BaseModel):
    username: str
    password: str


class CommentModel(BaseModel):
      content :str
      services:str





