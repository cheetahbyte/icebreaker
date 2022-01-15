import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # JWT - JSON Web Token
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES"))
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")