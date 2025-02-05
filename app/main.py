from fastapi import FastAPI
from app.database import init_db, close_db
from app.routes import orders, posts, products, users, protected

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()

app.include_router(users.router)
app.include_router(protected.router)
app.include_router(posts.router)
app.include_router(orders.router)
app.include_router(products.router)