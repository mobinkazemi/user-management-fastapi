from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import configparser


config = configparser.ConfigParser()
config.read("config.ini")

DB_HOST = config.get("database", "DB_HOST")

DB_PORT = config.get("database", "DB_PORT")

DB_NAME = config.get("database", "DB_NAME")

DB_USER = config.get("database", "DB_USER")

DB_PASSWORD = config.get("database", "DB_PASSWORD")


url = URL.create(
    drivername="postgresql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    database=DB_NAME,
    port=int(DB_PORT),
)

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
