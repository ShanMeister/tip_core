import json
import logging
import os
import re
import uuid
from datetime import datetime

from stix2 import Bundle, Indicator
from stix2.parsing import parse

from common.rabbitmq.rabbitmq import RabbitMQ
from stix.use_case.stix2_repository_interface import IStix2Repository

logger = logging.getLogger(__name__)


class Stix2Service:

    def __init__(self, stix2_repository: IStix2Repository, message_queue: RabbitMQ):
        self.repository = stix2_repository
        self.pattern_indicator = re.compile(r"'.*'")
        self.message_queue = message_queue

    def save_bundle(self, bundle_stix: Bundle):
        for stix_object in bundle_stix.get('objects'):
            try:
                stix = parse(stix_object)
                if stix.type == 'indicator':
                    self.save_indicator(stix)
            except Exception as e:
                logger.warning(f'process stix fail, error is {e} ,object is: {stix_object}')

    def save_indicator(self, indicator: Indicator):

        pattern = self.__extract_pattern(indicator)
        if pattern is None:
            return

        find_indicator = self.repository.find_indicator_by_pattern(pattern)
        if find_indicator is None:
            indicator_dict = self.__stix_to_dict(indicator.serialize())
        else:
            indicator_dict = self.__stix_to_dict(find_indicator.serialize())
            import_indicator_dict = self.__stix_to_dict(indicator.serialize())

            # update external_references
            source_list = []
            for item in indicator_dict['external_references']:
                source_list.append(item['source_name'])

            for item in import_indicator_dict['external_references']:
                if item['source_name'] not in source_list:
                    indicator_dict['external_references'].append(item)

            # update last_seen
            for key, value in import_indicator_dict['extensions'].items():
                if key in indicator_dict['extensions']:
                    connector_last_seen = value['last_seen']
                    if connector_last_seen is None:
                        indicator_dict['extensions'][key] = value
                        continue

                    if 'last_seen' in indicator_dict['extensions'][key]:
                        database_last_seen = indicator_dict['extensions'][key]['last_seen']
                        tmp_last_seen = list(set(database_last_seen + connector_last_seen))
                    else:
                        tmp_last_seen = connector_last_seen

                    indicator_dict['extensions'][key] = value
                    indicator_dict['extensions'][key]['last_seen'] = tmp_last_seen
                else:
                    indicator_dict['extensions'][key] = value

            # update valid_from
            indicator_dict['valid_from'] = min(
                [indicator_dict['valid_from']] + [v['valid_from'] for k, v in indicator_dict['extensions'].items()
                                                  if 'valid_from' in v and v['valid_from'] is not None])

            indicator_dict['modified'] = datetime.now()

        if indicator_dict is None:
            return

        self.repository.save_indicator(indicator_dict)
        if self.message_queue.is_valid():
            # TODO monitor status
            bundle = self.stix_to_bundle([indicator_dict])
            self.message_queue.produce(exchange_name=os.getenv('CHT_QUEUE_NOTIFY_ENRICHER', 'NOTIFY_ENRICHER_QUEUE'),
                                       queue_name=os.getenv('CHT_QUEUE_NOTIFY_ENRICHER', 'NOTIFY_ENRICHER_QUEUE'),
                                       data=bundle.serialize())

    def stix_to_bundle(self, stix_dict_list: list[dict]) -> Bundle:
        stix_list = []
        for item in stix_dict_list:
            stix_list.append(parse(item))

        return Bundle(id=f"bundle--{str(uuid.uuid4())}",
                      type="bundle",
                      objects=stix_list)

    def save_smo(self, smo):
        self.repository.save_smo(smo)
        return

    def __extract_pattern(self, indicator: Indicator):
        match_pattern = re.search(self.pattern_indicator, indicator.pattern)
        if match_pattern:
            return match_pattern.group()
        return None

    def __dict_to_str(self, dict_data: dict):
        dict_str = json.dumps(dict_data, default=str)
        # base64.b64encode(dict_str.encode('utf-8'))
        return dict_str

    def __stix_to_dict(self, stix_str: str) -> dict:
        return json.loads(stix_str)
