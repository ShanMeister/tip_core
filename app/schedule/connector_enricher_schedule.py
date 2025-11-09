import logging
import os
from datetime import datetime, timedelta

import pytz
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from common.rabbitmq.rabbitmq import RabbitMQ
from stix.repository.stix2_repository_elastic import Stix2RepositoryElastic
from stix.use_case.stix2_service import Stix2Service
from stix.use_case.stix2_validator import stix2Validator

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()

rabbit = RabbitMQ(host=os.getenv('CHT_MESSAGE_QUEUE_HOST', None),
                  port=os.getenv('CHT_MESSAGE_QUEUE_PORT', None),
                  account=os.getenv('CHT_MESSAGE_QUEUE_ACCOUNT', None),
                  password=os.getenv('CHT_MESSAGE_QUEUE_PWD', None),
                  heartbeat=1000)
service = Stix2Service(Stix2RepositoryElastic(), rabbit)
validator = stix2Validator()


def callback_consumer(channel, method, properties, body):
    try:
        service.save_bundle(validator.rabbit_body_to_stix(body))
    except ValueError as e:
        logger.warning(e, exc_info=1)
    except Exception as e:
        logger.error(e, exc_info=1)

    channel.basic_ack(delivery_tag=method.delivery_tag)


def consume_connector_schedule():
    logger.info('start consume connector')
    rabbit_schedule = RabbitMQ(host=os.getenv('CHT_MESSAGE_QUEUE_HOST', None),
                               port=os.getenv('CHT_MESSAGE_QUEUE_PORT', None),
                               account=os.getenv('CHT_MESSAGE_QUEUE_ACCOUNT', None),
                               password=os.getenv('CHT_MESSAGE_QUEUE_PWD', None),
                               heartbeat=1000)
    if rabbit_schedule.is_valid():
        rabbit_schedule.consume(queue_name=os.getenv('CHT_QUEUE_DATA_CONNECTION', 'CONNECTOR_DATA_QUEUE'),
                                exchange_name=os.getenv('CHT_QUEUE_DATA_CONNECTION', 'CONNECTOR_DATA_QUEUE'),
                                callback=callback_consumer)


def consume_enricher_schedule():
    logger.info('start consume enricher')
    rabbit_schedule = RabbitMQ(host=os.getenv('CHT_MESSAGE_QUEUE_HOST', None),
                               port=os.getenv('CHT_MESSAGE_QUEUE_PORT', None),
                               account=os.getenv('CHT_MESSAGE_QUEUE_ACCOUNT', None),
                               password=os.getenv('CHT_MESSAGE_QUEUE_PWD', None),
                               heartbeat=1000)
    if rabbit_schedule.is_valid():
        rabbit_schedule.consume(queue_name=os.getenv('CHT_QUEUE_DATA_ENRICHER', 'ENRICHER_DATA_QUEUE'),
                                exchange_name=os.getenv('CHT_QUEUE_DATA_ENRICHER', 'ENRICHER_DATA_QUEUE'),
                                callback=callback_consumer)


def produce_connector_schedule():
    logger.info('start produce connector')
    rabbit_schedule = RabbitMQ(host=os.getenv('CHT_MESSAGE_QUEUE_HOST', None),
                               port=os.getenv('CHT_MESSAGE_QUEUE_PORT', None),
                               account=os.getenv('CHT_MESSAGE_QUEUE_ACCOUNT', None),
                               password=os.getenv('CHT_MESSAGE_QUEUE_PWD', None),
                               heartbeat=1000)
    if rabbit_schedule.is_valid():
        # TODO monitor status
        bundle = service.stix_to_bundle([])
        rabbit_schedule.produce(exchange_name=os.getenv('CHT_QUEUE_NOTIFY_CONNECTION', 'NOTIFY_CONNECTOR_QUEUE'),
                                queue_name=os.getenv('CHT_QUEUE_NOTIFY_CONNECTION', 'NOTIFY_CONNECTOR_QUEUE'),
                                data=bundle.serialize())


def start_schedule_task():
    scheduler.add_jobstore(MemoryJobStore(), 'default')
    trigger_time = datetime.now() + timedelta(seconds=2)  # 2 秒後執行

    scheduler.add_job(
        consume_connector_schedule,
        run_date=trigger_time,
        id='consume_connector',
        name='Run consume_connector',
        replace_existing=True,
    )

    scheduler.add_job(
        consume_enricher_schedule,
        run_date=trigger_time,
        id='consume_enricher',
        name='Run consume_enricher',
        replace_existing=True,
    )

    trigger = CronTrigger(hour=0, minute=30, second=0, timezone=pytz.timezone('Asia/Taipei'))
    scheduler.add_job(
        produce_connector_schedule,
        trigger=trigger,
        id='produce_connector_schedule',
        name='Run consume_enricher',
        replace_existing=True,
    )

    scheduler.start()
