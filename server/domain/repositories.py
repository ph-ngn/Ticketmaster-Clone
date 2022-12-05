import datetime
from abc import ABC, abstractmethod
from typing import Optional
from .entities import *
from .value_objects import Username, Email


class IUserRepository(ABC):
    @abstractmethod
    def find_by_username(self, username: Username) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_by_email(self, email: Email) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def all(self) -> Optional[list[User]]:
        raise NotImplementedError

    @abstractmethod
    def add(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove(self, user: User) -> None:
        raise NotImplementedError


class IVenueRepository(ABC):
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Venue]:
        raise NotImplementedError

    @abstractmethod
    def add(self, venue: Venue) -> None:
        raise NotImplementedError


class IConcertRepository(ABC):
    @abstractmethod
    def find_by_concert_number(self, concert_number: float) -> Optional[Concert]:
        raise NotImplementedError

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[list[Concert]]:
        raise NotImplementedError

    @abstractmethod
    def find_by_venue(self, venue_name: Venue) -> Optional[list[Concert]]:
        raise NotImplementedError

    @abstractmethod
    def find_by_date(self, date: datetime.date) -> Optional[list[Concert]]:
        raise NotImplementedError

    @abstractmethod
    def all(self) -> Optional[list[Concert]]:
        raise NotImplementedError

    @abstractmethod
    def add(self, concert: Concert) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove(self, concert: Concert) -> None:
        raise NotImplementedError


class IOrderRepository(ABC):
    @abstractmethod
    def find_by_order_number(self, str: int):
        raise NotImplementedError

    @abstractmethod
    def add(self, order: Order):
        raise NotImplementedError
