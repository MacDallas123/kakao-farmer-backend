from dotenv import load_dotenv
import os


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "3ad36a2896073281ea99a646c88753f3942bdf4ff7d37a5500287da24bbd78da")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

