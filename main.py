from fastapi import FastAPI
import uvicorn
import routers.users as users
from database.database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
