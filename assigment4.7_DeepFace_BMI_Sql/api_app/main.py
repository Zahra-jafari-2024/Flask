from fastapi import FastAPI
from datetime import datetime 
import uvicorn

app=FastAPI()
@app.get("/")
def some_api():
    return {"date":datetime.date(datetime.now()) ,
            "day_name":  datetime.now().strftime("%A") ,
            "month_name" : datetime.now().strftime("%B"),
            }

if __name__ == "__main__":
    uvicorn.run(app ,port=8000 , host="127.0.0.1")