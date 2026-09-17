import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "1"))
    EXPOSE_DEV_OTP = os.getenv("EXPOSE_DEV_OTP", "false").lower() == "true"