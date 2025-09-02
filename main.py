from fastapi import FastAPI
from routers import todos,auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(todos.router)