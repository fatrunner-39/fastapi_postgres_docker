import uvicorn
from fastapi import FastAPI

from routers import likes, posts, users

app = FastAPI()


app.include_router(users.router, tags=['users'], prefix='/api/users')
app.include_router(posts.router, tags=['posts'], prefix='/api/posts')
app.include_router(likes.router, tags=['likes'], prefix='/api')


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host='0.0.0.0',
        port=8000, reload=True
    )
