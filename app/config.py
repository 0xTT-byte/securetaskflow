import os 

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
APP_ENV = os.getenv("APP_ENV", "development")

