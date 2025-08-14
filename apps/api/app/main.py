from fastapi import FastAPI

from app.api.routes import auth, users, projects
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)
