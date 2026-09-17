import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings


# Repo root, regardless of the working directory the app is started from
# (this file lives at <repo_root>/backend/Config/project_config.py).
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

class Project_config(BaseSettings):
    # database
    __DATABASE_URI_FORMAT: str = "{db_engine}://{user}:{password}@{host}:{port}/{database}"
    __DB_HOST: str = os.getenv("DB_HOST")
    __DB_USER: str = os.getenv("DB_USER")
    __DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    __DB_PORT: str = os.getenv("DB_PORT")
    __DB_ENGINE: str = os.getenv("DB_ENGINE")
    __DB_NAME: str = os.getenv("DB_NAME")

    # auth
    __SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")

    # CORS: lista separada por comas, ej. "https://miapp.com,http://localhost:5173"
    __CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "")


    # base
    @staticmethod
    def PROJECT_NAME() -> str:
        return "Agroclima api"


    @staticmethod
    def API_PREFIX() -> str:
        return "/api"


    # CORS: nunca "*" junto con allow_credentials=True — eso hace que el
    # navegador acepte credenciales desde cualquier origen. Configurar
    # CORS_ORIGINS en el .env con los orígenes reales del frontend.
    @staticmethod
    def BACKEND_CORS_ORIGINS() -> list[str]:
        # Los atributos "__x" son privados para pydantic: solo se resuelven
        # a su valor real sobre una instancia, no accedidos desde la clase.
        origins = Project_config().__CORS_ORIGINS
        if not origins:
            return []
        return [origin.strip() for origin in origins.split(",") if origin.strip()]

    @staticmethod
    def SECRET_KEY() -> str:
        secret = Project_config().__SECRET_KEY
        if not secret:
            raise RuntimeError(
                "Falta JWT_SECRET_KEY en el .env. Generar uno con: "
                "python -c \"import secrets; print(secrets.token_hex(32))\""
            )
        return secret


    @staticmethod
    def ALGORITHM() -> str:
        return "HS256"


    @staticmethod
    def OAUTH2_SCHEME() -> OAuth2PasswordBearer:
        return OAuth2PasswordBearer(tokenUrl="/api/auth/signIn")


    @property
    def DATABASE_URI(self) -> str:
        return self.__DATABASE_URI_FORMAT.format(
            db_engine=self.__DB_ENGINE,
            user=self.__DB_USER,
            password=self.__DB_PASSWORD,
            host=self.__DB_HOST,
            port=self.__DB_PORT,
            database=self.__DB_NAME,
        )