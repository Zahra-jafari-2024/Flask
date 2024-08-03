from fastapi import FastAPI
from database import User, RegisterModel, LoginModel, engine
from sqlmodel import Session , select 
app=FastAPI()


app.get("/users")
def get_numbers_user():
    with Session(engine) as session:
        statement = select(User)
        result = session.exec(statement)
        user_count = result.count()
        return {"user_count": user_count} 
