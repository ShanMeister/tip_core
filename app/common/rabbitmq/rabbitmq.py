import logging

import pika
from pika.adapters.blocking_connection import BlockingChannel

logger = logging.getLogger(__name__)


class RabbitMQ:

    def __init__(self, host: str, port: int, account: str, password: str, heartbeat: int):
        self.host = host
        self.port = port
        self.account = account
        self.password = password
        self.heartbeat = heartbeat
        credentials = pika.PlainCredentials(account, password)
        if self.is_valid():
            self.consume_connection = pika.BlockingConnection(
                pika.ConnectionParameters(heartbeat=self.heartbeat, host=self.host, port=self.port,
                                          credentials=credentials))

            self.producer_connection = pika.BlockingConnection(
                pika.ConnectionParameters(heartbeat=self.heartbeat, host=self.host, port=self.port,
                                          credentials=credentials))

    def is_valid(self):
        if self.host is not None and self.host != '' and \
                self.port is not None and self.port != '' and \
                self.account is not None and self.account != '' and \
                self.password is not None and self.password != '':
            return True

        return False

    def get_producer_channel(self) -> BlockingChannel:
        return self.producer_connection.channel()

    def get_consume_channel(self) -> BlockingChannel:
        return self.consume_connection.channel()

    def close_connection(self):
        if self.consume_connection:
            self.consume_connection.close()

        if self.produce_connection:
            self.produce_connection.close()

    def consume(self, exchange_name: str, queue_name: str, callback):
        channel = self.get_consume_channel()
        try:
            channel.queue_declare(queue_name, durable=True)
            channel.exchange_declare(exchange_name, durable=True)
            channel.queue_bind(queue=queue_name, exchange=exchange_name)
            channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
            channel.start_consuming()
        except Exception as e:
            logger.error(e, exc_info=1)

    def produce(self, exchange_name: str, queue_name: str, data: str):
        channel = self.get_producer_channel()
        try:
            channel.queue_declare(queue_name, durable=True)
            channel.exchange_declare(exchange_name, durable=True)
            channel.queue_bind(queue=queue_name, exchange=exchange_name)
            channel.basic_publish(exchange=exchange_name, routing_key=queue_name, body=data)
        except Exception as e:
            logger.error(e, exc_info=1)
