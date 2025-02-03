from tortoise import Tortoise, run_async

DB_URL = "sqlite://db.sqlite3"

async def init_db():
    await Tortoise.init(
        db_url=DB_URL,
        modules={"models": ["app.models"]}
    )
    await Tortoise.generate_schemas()

async def close_db():
    await Tortoise.close_connections()
