from tortoise import Tortoise, run_async
import os

#DB_URL = "postgres://user:password@localhost:5432/dbname"  # Modifiez avec vos informations
DB_URL = os.getenv("DATABASE_URL", "postgres://postgres:postgres@localhost:5432/kakao-farmer")

async def init_db():
    await Tortoise.init(
        db_url=DB_URL,
        modules={"models": ["app.models"]}
    )

    
    # Supprimer toutes les tables
    # await Tortoise._drop_databases() 

    # Créer toutes les tables
    await Tortoise.generate_schemas()

async def close_db():
    await Tortoise.close_connections()