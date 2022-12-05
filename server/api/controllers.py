import ast
from dependency_injector.wiring import inject, Provide
from flask_restful.reqparse import RequestParser
from flask import jsonify, request
from flask.views import MethodView
from domain.services import *
from domain.dtos import *
from infra.ioc_container import IocContainer
from .exceptions import APIException
from .services import JWTService, login_required, params_required, get_skip_and_limit, get_search
from .err_http_mapper import http_code_mapper


class SignUpController(MethodView):
    @inject
    def __init__(self,
                 user_service: UserService = Provide[IocContainer.user_service],
                 parser: RequestParser = Provide[IocContainer.parser]):
        self._user_service = user_service
        self._parser = parser
        self._parser.add_argument('username', type=str, required=True, help='username is required')
        self._parser.add_argument('email', type=str, required=True, help='email is required')
        self._parser.add_argument('password', type=str, required=True, help='password is required')
        self._parser.add_argument('account_type', type=str, required=True, help='account type is required')
        self._parser.add_argument('secret_key', type=str, help='key must be a string')

    def post(self):
        req_body = self._parser.parse_args()
        req = RegisterUserRequest(**req_body)
        res = self._user_service.register_user(req)
        if isinstance(res, ErrorResponse):
            raise APIException(res.message, http_code_mapper(res.err_type))

        return jsonify(res.to_dict()), 201


class LogInController(MethodView):
    @inject
    def __init__(self,
                 user_service: UserService = Provide[IocContainer.user_service],
                 parser: RequestParser = Provide[IocContainer.parser]):
        self._user_service = user_service
        self._parser = parser
        self._parser.add_argument('email', type=str, required=True, help='email is required')
        self._parser.add_argument('password', type=str, required=True, help='password is required')

    def post(self):
        req_body = self._parser.parse_args()
        req = GetUserIdentityRequest(**req_body)
        res = self._user_service.get_user_identity(req)
        if isinstance(res, ErrorResponse):
            raise APIException(res.message, http_code_mapper(res.err_type))
        token = JWTService.generate_jwt(res.username, res.account_type)
        return jsonify({'token': token}), 200


class VenueController(MethodView):
    def __init__(self,
                 venue_service: VenueService = Provide[IocContainer.venue_service],
                 parser: RequestParser = Provide[IocContainer.parser]):
        self._venue_service = venue_service
        self._parser = parser
        self._parser.add_argument('name', type=str, required=True, help='name is required')
        self._parser.add_argument('seat_offering', type=dict, required=True, help='seat_offering is required')

    @login_required
    def post(self, *args, **kwargs):
        req_body = self._parser.parse_args()
        req = RegisterVenueRequest(**req_body)
        res = self._venue_service.register_venue(req)
        if isinstance(res, ErrorResponse):
            raise APIException(res.message, http_code_mapper(res.err_type))

        return jsonify(res.to_dict()), 201


class ConcertController(MethodView):
    @inject
    def __init__(self,
                 concert_service: ConcertService = Provide[IocContainer.concert_service],
                 parser: RequestParser = Provide[IocContainer.parser],
                 s3_bucket = Provide[IocContainer.s3_bucket]):
        self._concert_service = concert_service
        self._parser = parser
        self._s3_bucket = s3_bucket
        self._parser.add_argument('name', type=str, required=True, help='name is required', location='form')
        self._parser.add_argument('venue', type=str, required=True, help='venue is required', location='form')
        self._parser.add_argument('date', type=str, required=True, help='date is required', location='form')
        self._parser.add_argument('seat_offering', type=str, location='form')
        self._parser.add_argument('pricing', type=str, location='form')


    @login_required
    def post(self, user, *args, **kwargs):
        req_body = self._parser.parse_args()
        imgs = request.files.getlist("posters[]")
        urls = self._s3_bucket.upload_files(imgs, user)
        req_body.update({'seat_offering': ast.literal_eval(req_body['seat_offering']),
                         'pricing': ast.literal_eval(req_body['pricing']),
                         'posters_urls': urls})
        req = BookConcertRequest(user, **req_body)
        res = self._concert_service.book_concert(req)
        if isinstance(res, ErrorResponse):
            raise APIException(res.message, http_code_mapper(res.err_type))

        return jsonify(res.to_dict()), 201

    def get(self):
        skip, limit = get_skip_and_limit()
        search = get_search()
        if search:
            name_sub = self._concert_service.get_concerts_by_name(search)
            venue_sub = self._concert_service.get_concerts_by_venue(search)
            query = [concert for subquery in (name_sub, venue_sub) if not isinstance(subquery, ErrorResponse) for concert in subquery]
        else:
            query = self._concert_service.get_all_concerts(skip, limit)
        return jsonify([concert.to_dict() for concert in query]), 200


class ConcertManagerController(MethodView):
    @inject
    def __init__(self,
                 concert_service: ConcertService = Provide[IocContainer.concert_service],
                 parser: RequestParser = Provide[IocContainer.parser]):
        self._concert_service = concert_service
        self._parser = parser
        self._parser.add_argument('name', type=str)
        self._parser.add_argument('venue', type=str)
        self._parser.add_argument('date', type=str)
        self._parser.add_argument('seat_offering', type=dict)
        self._parser.add_argument('pricing', type=dict)

    @login_required
    def get(self, user, concert_number, *args, **kwargs):
        if concert_number:
            res = self._concert_service.get_concert_by_number(concert_number)
            if isinstance(res, ErrorResponse):
                raise APIException(res.message, http_code_mapper(res.err_type))
            return jsonify(res.to_dict()), 200
        else:
            res = self._concert_service.get_concerts_by_promoter(user)
            if isinstance(res, ErrorResponse):
                raise APIException(res.message, http_code_mapper(res.err_type))
            return jsonify([concert.to_dict() for concert in res]), 200

    @login_required
    @params_required
    def put(self, user, concert_number, *args, **kwargs):
        req_body = self._parser.parse_args()
        if not all(req_body.values()):
            raise APIException("All fields are required for PUT method", 400)
        req = UpdateConcertRequest(user, concert_number, req_body)
        res = self._concert_service.update_concert(req)
        if isinstance(res, ErrorResponse):
            raise APIException(res.message, http_code_mapper(res.err_type))

        return jsonify(res.to_dict()), 200

    @login_required
    @params_required
    def patch(self, user, concert_number, *args, **kwargs):
        req_body = self._parser.parse_args()
        req = UpdateConcertRequest(user, concert_number, {k: v for k, v in req_body.items() if v is not None})
        res = self._concert_service.update_concert(req)
        if isinstance(res, ErrorResponse):
            raise APIException(res.message, http_code_mapper(res.err_type))

        return jsonify(res.to_dict()), 200

    @login_required
    @params_required
    def delete(self, user, concert_number, *args, **kwargs):
        res = self._concert_service.remove_concert(user, concert_number)
        if isinstance(res, ErrorResponse):
            raise APIException(res.message, http_code_mapper(res.err_type))

        return jsonify({"message": "Concert is successfully removed"}, 200)


class DraftOrderController(MethodView):
    def __init__(self,
                 order_service: OrderService = Provide[IocContainer.order_service],
                 parser: RequestParser = Provide[IocContainer.parser]):
        self._order_service = order_service
        self._parser = parser
        self._parser.add_argument('concert', type=str, required=True, help='concert is required')
        self._parser.add_argument('currency', type=str, required=True, help='currency is required')
        self._parser.add_argument('order_items', type=dict, required=True, help='order_item is required')

    @login_required
    def post(self, user, *args, **kwargs):
        req_body = self._parser.parse_args()
        req = PlaceDraftOrderRequest(user, **req_body)
        res = self._order_service.place_draft_order(req)
        if isinstance(res, ErrorResponse):
            raise APIException(res.message, http_code_mapper(res.err_type))

        return jsonify(res.to_dict()), 201
