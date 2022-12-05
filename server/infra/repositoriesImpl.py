from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from pymongo.errors import DuplicateKeyError
from domain.entities import *
from domain.repositories import *
from domain.value_objects import *
from domain.exceptions import DBIntegrityError, NotExist
from .db import db_session, concerts_collection, venues_collection, orders_collection


class UserRepository(IUserRepository):
    def __init__(self, _db_session=db_session):
        self._db = _db_session

    def find_by_username(self, username) -> Optional[User]:
        query = self._db.query(User).filter_by(username=username).first()
        if not query:
            raise NotExist("User does not exist")
        return query

    def find_by_email(self, email) -> Optional[User]:
        query = self._db.query(User).filter_by(email=email).first()
        if not query:
            raise NotExist("User does not exist")
        return query

    def all(self) -> Optional[List[User]]:
        return self._db.query(User).all()

    def add(self, user: User) -> None:
        try:
            self._db.add(user)
            self._db.commit()
        except IntegrityError:
            raise DBIntegrityError('Username/Email already exist(s)')

    def remove(self, user: User) -> None:
        self._db.delete(user)
        self._db.commit()


class VenueRepository(IVenueRepository):
    def __init__(self, collection=venues_collection):
        self._collection = collection

    def find_by_name(self, name: str):
        query = self._collection.find_one({"name": name}, {'_id': False})
        if not query:
            raise NotExist("Venue with this name doesn't exist")
        return Venue(**query)

    def add(self, venue: Venue) -> None:
        try:
            self._collection.insert_one(venue.to_dict())
        except DuplicateKeyError:
            raise DBIntegrityError('Venue with this name already exists')


class ConcertRepository(IConcertRepository):
    def __init__(self, collection=concerts_collection):
        self._collection = collection

    def find_by_concert_number(self, concert_number: str) -> Optional[Concert]:
        query = self._collection.find_one({"concert_number": concert_number}, {'_id': False})
        if not query:
            raise NotExist("Concert with this number doesn't exist")
        return Concert(**query)

    def find_by_promoter(self, promoter: str) -> Optional[List[Concert]]:
        query = self._collection.find({"promoter": promoter}, {"_id": False})
        return [Concert(**data) for data in query]

    def find_by_name(self, name: str) -> Optional[list[Concert]]:
        query = self._collection.find({"name": {"$regex": name, '$options': 'i'}}, {"_id": False})
        return [Concert(**data) for data in query]

    def find_by_venue(self, venue: str) -> Optional[List[Concert]]:
        query = self._collection.find({"venue": {"$regex": venue, '$options': 'i'}}, {"_id": False})
        return [Concert(**data) for data in query]

    def find_by_date(self, date: datetime.date) -> Optional[List[Concert]]:
        query = self._collection.find({"date": {"$regex": str(date), '$options': 'i'}}, {"_id": False})
        return [Concert(**data) for data in query]

    def update(self, concert: Concert):
        self._collection.update_one({"concert_number": concert.concert_number}, {"$set": concert.to_dict()})

    def all(self, skip, limit) -> list[Optional[Concert]]:
        query = self._collection.find({}, {'_id': False}).skip(skip).limit(limit)
        return [Concert(**data) for data in query]

    def add(self, concert: Concert) -> None:
        self._collection.insert_one(concert.to_dict())

    def remove(self, concert: Concert) -> None:
        self._collection.delete_one({"concert_number": concert.concert_number})


class OrderRepository(IOrderRepository):
    def __init__(self, collection=orders_collection):
        self._collection = collection

    def find_by_order_number(self, order_number: str):
        query = self._collection.find_one({"order_number": order_number}, {"_id": False})
        if not query:
            raise NotExist("Order with this number does not exist")
        tickets = set(Ticket(**subquery) for subquery in query['tickets'])
        query['tickets'] = tickets
        return Order(**query)

    def update(self, order: Order):
        self._collection.update_one({"order_number": order.order_number}, {'$set': order.to_dict()})

    def add(self, order: Order) -> None:
        self._collection.insert_one(order.to_dict())
