from flask import Flask, jsonify
from flask_cors import CORS
from infra.db import db_session,  init_db
from infra.ioc_container import IocContainer
from infra.message_consumer import Consumer, CompletedOrderHandler
from api.controllers import *
from api.exceptions import APIException


def create_server():
    server = Flask(__name__)
    CORS(server)
    init_db()
    server.container = IocContainer()
    server.config['BUNDLE_ERRORS'] = True

    @server.teardown_request
    def remove_session(exception=None):
        db_session.remove()

    @server.errorhandler(APIException)
    def generic_api_exception(e):
        return jsonify(e.to_dict()), e.status_code

    server.add_url_rule('/signup', view_func=SignUpController.as_view('register_api'))
    server.add_url_rule('/login', view_func=LogInController.as_view('login_api'))
    server.add_url_rule('/venues', view_func=VenueController.as_view('venue_api'))
    server.add_url_rule('/concerts', view_func=ConcertController.as_view('concert_api'))
    server.add_url_rule('/orders', view_func=DraftOrderController.as_view('order_api'))
    server.add_url_rule('/concerts/', defaults={'concert_number': None}, view_func=ConcertManagerController.as_view('concert_manager_api_default'))
    server.add_url_rule('/concerts/<string:concert_number>', view_func=ConcertManagerController.as_view('concert_manager_api'))

    return server


def main():
    server = create_server()
    consumer = Consumer(auto_commit_interval_ms=1000, enable_auto_commit=True,)
    consumer.add_event_handler('completedOrder', CompletedOrderHandler().handle)
    consumer.start()

    server.run(debug=True)


if __name__ == '__main__':
    main()