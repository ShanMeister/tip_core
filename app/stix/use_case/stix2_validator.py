import json
import logging

from stix2 import Bundle
from stix2.parsing import dict_to_stix2

logger = logging.getLogger(__name__)


class stix2Validator:

    def rabbit_body_to_stix(self, bundle_body) -> Bundle:
        body_dict = json.loads(bundle_body)
        logger.info(f"test body {body_dict}")
        try:
            bundle_stix2 = dict_to_stix2(body_dict, allow_custom=True)
        except Exception as e:
            raise ValueError('parse dict to stix2 error')

        return bundle_stix2
