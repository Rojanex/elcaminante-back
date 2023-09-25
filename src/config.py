import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    def __init__(self) -> None:
        self.DB_NAME = os.environ.get('DB_NAME')
        self.DB_PASS = os.environ.get('DB_PASS')
        self.SECRET_KEY = os.environ.get('SECRET_KEY')

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        db_uri = f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return db_uri