from fastapi import FastAPI

from app.api.routes import (
    auth,
    users,
    projects,
    files,
    notifications,
    analytics,
    tasks,
    search,
)
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(files.router)
app.include_router(notifications.router)
app.include_router(analytics.router)
app.include_router(tasks.router)
app.include_router(search.router)
