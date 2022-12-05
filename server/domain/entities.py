import hmac
import hashlib
import datetime
import uuid
from typing import Iterator
from . import config
from .mixins import *
from .value_objects import *


class User(ToDictMixin):
    def __init__(self,
                 username,
                 email,
                 password,
                 account_type,
                 secret_key,
                 is_active=True,
                 created_at: datetime = None):
        self.username = Username(username).validated_data
        self.email = Email(email).validated_data
        self._password = self.__class__._hash_password(Password(password).validated_data)
        self.account_type = AccountType(account_type, secret_key).validated_data
        self.is_active = is_active
        self.created_at = created_at if created_at else datetime.datetime.now()

    def check_password(self, password) -> bool:
        matched = self._password == self.__class__._hash_password(password)
        if not matched:
            raise InvalidUserIdentity

    @staticmethod
    def _hash_password(password):
        return hmac.new(config.get('SECRET_KEY').encode(), password.encode(), hashlib.sha256) \
            .hexdigest().upper()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = self.__class__._hash_password(password)

    def __repr__(self):
        return f'<User: {self.username} / {self.email} | ' \
               f'Account Type: {self.account_type} | ' \
               f'Created At: {self.created_at}>'


class Venue(ToDictMixin):
    def __init__(self, name, seat_offering):
        self.name = name
        self.seat_offering = seat_offering

    def update_seat_offering(self, **kwargs):
        self.seat_offering.update(kwargs)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.name == other.name and self.seat_offering == other.seat_offering

    def __repr__(self):
        return f'<Venue: {self.name} | ' + ', '.join([f'{v} {k}' for k, v in self.seat_offering.items()])


class Concert(ToDictMixin):
    def __init__(self,
                 promoter: str,
                 name: str,
                 venue: str,
                 date: str,
                 seat_offering: dict,
                 pricing: dict,
                 posters_urls: list,
                 concert_number: uuid.UUID = None):
        self.concert_number = concert_number if concert_number else str(uuid.uuid4().int)
        self.promoter = promoter
        self.name = name
        self.venue = venue
        self.date = ISODate(date).validated_data
        self.seat_offering = seat_offering
        self.pricing = pricing
        self.posters_urls = posters_urls

    def __hash__(self):
        return hash(self.concert_number)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.concert_number == other.concert_number


    def reserve_seats(self, order_items: dict):
        for k, v in order_items.items():
            self.seat_offering[k] -= v

    def update(self, **kwargs):
        if not set(kwargs).issubset(self.to_dict()):
            raise IncompatibleUpdate
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return f'<Concert: {self.name} | ' \
               f'Venue: {self.venue} | ' \
               f'Date: {self.date} | ' \
               f'Seat Offering: {[f"{v} {k}" for k, v in self.seat_offering.items()]}>'


class Ticket(ToDictMixin):
    def __init__(self,
                 seat_type: str,
                 price: int,
                 ticket_number: uuid.UUID = None):
        self.ticket_number = ticket_number if ticket_number else str(uuid.uuid4().int)
        self.seat_type = seat_type
        self.price = price

    def __repr__(self):
        return f'<Ticket: {self.ticket_number} | ' \
               f'Seat Type: {self.seat_type} | ' \
               f'Price: {self.price}>'

    def __hash__(self):
        return hash(self.ticket_number)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.ticket_number == other.ticket_number


# Aggregate root
class Order(ToDictMixin):
    def __init__(self,
                 concert_number: uuid.UUID,
                 concert_name: str,
                 consumer: str,
                 currency: str,
                 total: float = 0,
                 state: str = 'pending',
                 last_processed_at: datetime = None,
                 order_number: uuid.UUID = None,
                 tickets: set[Ticket] = None):
        self.order_number = order_number if order_number else str(uuid.uuid4().int)
        self.concert_number = concert_number
        self.concert_name = concert_name
        self.consumer = consumer
        self.total = total
        self.currency = Currency(currency).validated_data
        self.last_processed_at = last_processed_at if last_processed_at else datetime.datetime.now()
        self.state = state
        self.tickets = tickets if tickets else set()

    def add_ticket(self, ticket: Ticket):
        self.tickets.add(ticket)
        self.total += ticket.price

    def add_tickets(self, tickets: Iterator[Ticket]):
        for ticket in tickets:
            self.add_ticket(ticket)

    def finalize(self):
        self.state = 'completed'
        self.last_processed_at = datetime.datetime.now()

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if attr in self.to_dict():
                setattr(self, attr, value)

    def remove_ticket(self, ticket: Ticket):
        self.tickets.remove(ticket)

    def __repr__(self):
        return f'<Order: {self.order_number} | ' \
               f'Total: {self.total} {self.currency} | ' \
               f'State: {self.state} | ' \
               f'Last Processed At: {self.last_processed_at}>'
