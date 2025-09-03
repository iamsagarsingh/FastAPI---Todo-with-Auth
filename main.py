from fastapi import FastAPI
from routers import todos,auth,users

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)