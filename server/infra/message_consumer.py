import logging
import threading
import json
from kafka import KafkaConsumer
from kafka import TopicPartition
from dependency_injector.wiring import inject, Provide
from domain.services import OrderService
from .ioc_container import IocContainer


class Consumer(threading.Thread):
    def __init__(self, **kwargs):
        super().__init__()
        self.daemon = True
        self._stop_event = threading.Event()
        self._consumer = KafkaConsumer(**kwargs)
        self._logger = logging.getLogger('kafka-consumer')
        self._logger.setLevel(logging.INFO)
        self._handlers = {}

    def add_event_handler(self, topic, handler):
        if self._handlers.get(topic) is None:
            self._handlers[topic] = []
        self._handlers[topic].append(handler)

    def _run_event_handlers(self, msg):
        try:
            handlers = self._handlers[msg.topic]
            for handler in handlers:
                handler(msg)
        except KeyError:
            self._logger.critical('No handler found for this topic')
            self._consumer.close()

    def stop(self):
        self._stop_event.set()

    def run(self):
        self._consumer.assign([TopicPartition(topic, 0) for topic in self._handlers.keys()])
        self._logger.info(f"Starting consumer")
        while not self._stop_event.is_set():
            for msg in self._consumer:
                self._logger.info(f"Topic: {msg.topic} | Payload: {msg.value}")
                self._run_event_handlers(msg)


class CompletedOrderHandler:
    @inject
    def __init__(self, order_service: OrderService = Provide[IocContainer.order_service]):
        self._order_service = order_service

    def handle(self, msg):
        decoded_data = json.loads(msg.value)
        self._order_service.finalize_order(decoded_data['order_number'])
