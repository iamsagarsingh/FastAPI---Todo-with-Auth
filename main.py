from fastapi import FastAPI
from routers import todos

app = FastAPI()


app.include_router(todos.router)