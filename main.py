from fastapi import FastAPI
import uvicorn
import routers.users as users
from database.database import engine, Base
import routers.token as routes

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(routes.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
