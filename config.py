import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    USER = os.environ.get('USER')
    EMAIL = os.environ.get('EMAIL')
    PASSWORD = os.environ.get('PASSWORD')
    GIT_KEY = os.environ.get('GIT_KEY') or None
