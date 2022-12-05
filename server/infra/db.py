from uuid import uuid4
from sqlalchemy import create_engine, MetaData, Table, Column, String, Boolean, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from pymongo import MongoClient
from domain.entities import User

engine = create_engine('sqlite:////tmp/test.db')
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


def init_db():
    metadata.create_all(bind=engine)


users_table = Table('users', metadata,
                    Column('_id', String, primary_key=True, default=lambda: str(uuid4())),
                    Column('username', String(50), unique=True),
                    Column('email', String(120), unique=True),
                    Column('_password', String()),
                    Column('account_type', String(20)),
                    Column('is_active', Boolean()),
                    Column('created_at', DateTime()))

mapper(User, users_table)

mongodb_connection = "mongodb+srv://project1:project1@project1.eggrmcz.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongodb_connection)

db = client.project1
concerts_collection = db.concerts
venues_collection = db.venues
orders_collection = db.orders
