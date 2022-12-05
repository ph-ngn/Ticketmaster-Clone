from dataclasses import dataclass


@dataclass
class ErrorResponse:
    err_type: str
    message: str


@dataclass
class RegisterUserRequest:
    username: str
    email: str
    password: str
    account_type: str
    secret_key: str = None


@dataclass
class GetUserIdentityRequest:
    email: str
    password: str


@dataclass
class RegisterVenueRequest:
    name: str
    seat_offering: dict


@dataclass
class GetVenueByNameRequest:
    name: str


@dataclass
class BookConcertRequest:
    promoter: str
    name: str
    venue: str
    date: str
    seat_offering: dict
    pricing: dict
    posters_urls: list


@dataclass
class PlaceDraftOrderRequest:
    consumer: str
    concert: str
    currency: str
    order_items: dict


@dataclass
class UpdateConcertRequest:
    promoter: str
    concert_number: str
    update_fields: dict

