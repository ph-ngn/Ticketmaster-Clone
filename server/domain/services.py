from typing import Optional, Union
from .repositories import *
from .exceptions import *
from .dtos import *
from .value_objects import *


class UserService:
    def __init__(self, user_repo: IUserRepository):
        self._repo = user_repo

    def register_user(self, req: RegisterUserRequest) -> Union[User, ErrorResponse]:
        try:
            user = User(**req.__dict__)
            # copy of user to prevent repo.add from including id in the response
            user_res = user
            self._repo.add(user)
            return user_res
        except (InvalidUsername,
                InvalidEmail,
                InvalidPassword,
                InvalidAccountType,
                InvalidSecretKey,
                DBIntegrityError) as e:
            return ErrorResponse(type(e).__name__, e.message)

    def get_user_identity(self, req: GetUserIdentityRequest) -> Union[User, ErrorResponse]:
        try:
            email = Email(req.email)
            user = self._repo.find_by_email(email.validated_data)
            if user:
                user.check_password(req.password)
                return user
        except (InvalidEmail, InvalidUserIdentity, NotExist) as e:
            return ErrorResponse(type(e).__name__, e.message)


class VenueService:
    def __init__(self, venue_repo: IVenueRepository):
        self._repo = venue_repo

    def register_venue(self, req: RegisterVenueRequest) -> Union[Venue, ErrorResponse]:
        try:
            venue = Venue(**req.__dict__)
            self._repo.add(venue)
            return venue
        except DBIntegrityError as e:
            return ErrorResponse(type(e).__name__, e.message)

    def get_venue_by_name(self, name) -> Union[Venue, ErrorResponse]:
        try:
            venue = self._repo.find_by_name(name)
            return venue
        except NotExist as e:
            return ErrorResponse(type(e).__name__, e.message)


class ConcertService:
    def __init__(self, concert_repo: IConcertRepository, venue_repo: IVenueRepository):
        self._concert_repo = concert_repo
        self._venue_repo = venue_repo

    def book_concert(self, req: BookConcertRequest) -> Union[Concert, ErrorResponse]:
        try:
            venue = self._venue_repo.find_by_name(req.venue)
            SeatOfferingBenchmark(req.seat_offering, venue.to_dict())
            req.venue = venue.name
            concert = Concert(**vars(req))
            self._concert_repo.add(concert)
            return concert
        except (IncompatibleSeatOffering, InvalidDateFormat, PastDate, NotExist) as e:
            return ErrorResponse(type(e).__name__, e.message)

    def get_all_concerts(self, skip, limit) -> list[Optional[Concert]]:
        return self._concert_repo.all(skip, limit)

    def get_concert_by_number(self, concert_number) -> Union[Concert, ErrorResponse]:
        try:
            concert = self._concert_repo.find_by_concert_number(concert_number)
            return concert
        except NotExist as e:
            return ErrorResponse(type(e).__name__, e.message)

    def get_concerts_by_promoter(self, promoter) -> Union[list[Concert], ErrorResponse]:
        try:
            concerts = self._concert_repo.find_by_promoter(promoter)
            return concerts
        except NotExist as e:
            return ErrorResponse(type(e).__name__, e.message)

    def get_concerts_by_name(self, name) -> Union[list[Concert], ErrorResponse]:
        try:
            concerts = self._concert_repo.find_by_name(name)
            return concerts
        except NotExist as e:
            return ErrorResponse(type(e).__name__, e.message)

    def get_concerts_by_venue(self, venue) -> Union[list[Concert], ErrorResponse]:
        try:
            concerts = self._concert_repo.find_by_venue(venue)
            return concerts
        except NotExist as e:
            return ErrorResponse(type(e).__name__, e.message)

    def update_concert(self, req: UpdateConcertRequest) -> Union[Concert, ErrorResponse]:
        try:
            concert = self._concert_repo.find_by_concert_number(req.concert_number)
            if req.promoter != concert.promoter:
                raise Unauthorized
            concert.update(**req.update_fields)
            self._concert_repo.update(concert)
            return concert
        except (NotExist, IncompatibleUpdate, Unauthorized) as e:
            return ErrorResponse(type(e).__name__, e.message)

    def remove_concert(self, promoter, concert_number) -> Optional[ErrorResponse]:
        try:
            concert = self._concert_repo.find_by_concert_number(concert_number)
            if promoter != concert.promoter:
                raise Unauthorized
            self._concert_repo.remove(concert)
        except (NotExist, Unauthorized) as e:
            return ErrorResponse(type(e).__name__, e.message)


class OrderService:
    def __init__(self, order_repo: IOrderRepository, concert_repo: IConcertRepository):
        self._order_repo = order_repo
        self._concert_repo = concert_repo

    def place_draft_order(self, req: PlaceDraftOrderRequest) -> Union[Order, ErrorResponse]:
        try:
            concert = self._concert_repo.find_by_concert_number(req.concert)
            order_items = SeatOfferingBenchmark(req.order_items, concert.to_dict())
            order = Order(concert.concert_number,
                          concert.name,
                          req.consumer,
                          req.currency)
            order.add_tickets(Ticket(k, concert.pricing[k]) for k, v in order_items.validated_data.items() for _ in range(v))
            self._order_repo.add(order)
            return order
        except (UnsupportedCurrency, IncompatibleSeatOffering, NotExist) as e:
            return ErrorResponse(type(e).__name__, e.message)

    def finalize_order(self, order_number):
        try:
            order = self._order_repo.find_by_order_number(order_number)
            concert = self._concert_repo.find_by_concert_number(order.concert_number)

            order.finalize()
            order_items = {}
            for ticket in order.tickets:
                if ticket.seat_type not in order_items:
                    order_items[ticket.seat_type] = 0
                order_items[ticket.seat_type] += 1

            concert.reserve_seats(order_items)
            self._order_repo.update(order)
            self._concert_repo.update(concert)

        except NotExist as e:
            return ErrorResponse(type(e).__name__, e.message)
