import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    def __init__(self) -> None:
        self.SECRET_KEY = os.environ.get('SECRET_KEY')

  