import os
from datetime import datetime

from stix2 import ExtensionDefinition

apwg_extension_definition = ExtensionDefinition(id=str(os.getenv('HISTORY_EXTENSION_DEFINITION_ID')),
                                                name=str(
                                                    os.getenv('HISTORY_EXTENSION_DEFINITION_NAME')),
                                                schema=str(
                                                    os.getenv('HISTORY_EXTENSION_DEFINITION_SCHEMA')),
                                                version='1',
                                                created_by_ref=str(
                                                    os.getenv(
                                                        'HISTORY_EXTENSION_DEFINITION_CREATE_BY')),
                                                extension_types=['property-extension'],
                                                created=datetime.strptime(os.getenv(
                                                    'HISTORY_EXTENSION_DEFINITION_CREATE_DATE'),
                                                    '%Y-%m-%d'),
                                                modified=datetime.strptime(os.getenv(
                                                    'HISTORY_EXTENSION_DEFINITION_MODIFY_DATE'),
                                                    '%Y-%m-%d')
                                                )

proofpoint_extension_definition = ExtensionDefinition(id=str(os.getenv('PROOFPOINT_EXTENSION_DEFINITION_ID')),
                                                      name=str(
                                                          os.getenv('PROOFPOINT_EXTENSION_DEFINITION_NAME')),
                                                      schema=str(
                                                          os.getenv('PROOFPOINT_EXTENSION_DEFINITION_SCHEMA')),
                                                      version='1',
                                                      created_by_ref=str(
                                                          os.getenv(
                                                              'PROOFPOINT_EXTENSION_DEFINITION_CREATE_BY')),
                                                      extension_types=['property-extension'],
                                                      created=datetime.strptime(os.getenv(
                                                          'PROOFPOINT_EXTENSION_DEFINITION_CREATE_DATE'),
                                                          '%Y-%m-%d'),
                                                      modified=datetime.strptime(os.getenv(
                                                          'PROOFPOINT_EXTENSION_DEFINITION_MODIFY_DATE'),
                                                          '%Y-%m-%d')
                                                      )

nisac_extension_definition = ExtensionDefinition(id=str(os.getenv('NISAC_EXTENSION_DEFINITION_ID')),
                                                 name=str(
                                                     os.getenv('NISAC_EXTENSION_DEFINITION_NAME')),
                                                 schema=str(
                                                     os.getenv('NISAC_EXTENSION_DEFINITION_SCHEMA')),
                                                 version='1',
                                                 created_by_ref=str(
                                                     os.getenv(
                                                         'NISAC_EXTENSION_DEFINITION_CREATE_BY')),
                                                 extension_types=['property-extension'],
                                                 created=datetime.strptime(os.getenv(
                                                     'NISAC_EXTENSION_DEFINITION_CREATE_DATE'),
                                                     '%Y-%m-%d'),
                                                 modified=datetime.strptime(os.getenv(
                                                     'NISAC_EXTENSION_DEFINITION_MODIFY_DATE'),
                                                     '%Y-%m-%d')
                                                 )

cht_misp_soc_extension_definition = ExtensionDefinition(id=str(os.getenv('CHT_MISP_SOC_EXTENSION_DEFINITION_ID')),
                                                        name=str(
                                                            os.getenv('CHT_MISP_SOC_EXTENSION_DEFINITION_NAME')),
                                                        schema=str(
                                                            os.getenv('CHT_MISP_SOC_EXTENSION_DEFINITION_SCHEMA')),
                                                        version='1',
                                                        created_by_ref=str(
                                                            os.getenv(
                                                                'CHT_MISP_SOC_EXTENSION_DEFINITION_CREATE_BY')),
                                                        extension_types=['property-extension'],
                                                        created=datetime.strptime(os.getenv(
                                                            'CHT_MISP_SOC_EXTENSION_DEFINITION_CREATE_DATE'),
                                                            '%Y-%m-%d'),
                                                        modified=datetime.strptime(os.getenv(
                                                            'CHT_MISP_SOC_EXTENSION_DEFINITION_MODIFY_DATE'),
                                                            '%Y-%m-%d')
                                                        )

cht_ir_extension_definition = ExtensionDefinition(id=str(os.getenv('CHT_IR_EXTENSION_DEFINITION_ID')),
                                                  name=str(
                                                      os.getenv('CHT_IR_EXTENSION_DEFINITION_NAME')),
                                                  schema=str(
                                                      os.getenv('CHT_IR_EXTENSION_DEFINITION_SCHEMA')),
                                                  version='1',
                                                  created_by_ref=str(
                                                      os.getenv(
                                                          'CHT_IR_EXTENSION_DEFINITION_CREATE_BY')),
                                                  extension_types=['property-extension'],
                                                  created=datetime.strptime(os.getenv(
                                                      'CHT_IR_EXTENSION_DEFINITION_CREATE_DATE'),
                                                      '%Y-%m-%d'),
                                                  modified=datetime.strptime(os.getenv(
                                                      'CHT_IR_EXTENSION_DEFINITION_MODIFY_DATE'),
                                                      '%Y-%m-%d')
                                                  )

virustotal_extension_definition = ExtensionDefinition(id=str(os.getenv('VIRUSTOTAL_EXTENSION_DEFINITION_ID')),
                                                      name=str(
                                                          os.getenv('VIRUSTOTAL_EXTENSION_DEFINITION_NAME')),
                                                      schema=str(
                                                          os.getenv('VIRUSTOTAL_EXTENSION_DEFINITION_SCHEMA')),
                                                      version='1',
                                                      created_by_ref=str(
                                                          os.getenv(
                                                              'VIRUSTOTAL_EXTENSION_DEFINITION_CREATE_BY')),
                                                      extension_types=['property-extension'],
                                                      created=datetime.strptime(os.getenv(
                                                          'VIRUSTOTAL_EXTENSION_DEFINITION_CREATE_DATE'),
                                                          '%Y-%m-%d'),
                                                      modified=datetime.strptime(os.getenv(
                                                          'VIRUSTOTAL_EXTENSION_DEFINITION_MODIFY_DATE'),
                                                          '%Y-%m-%d')
                                                      )

markmonitor_extension_definition = ExtensionDefinition(id=str(os.getenv('MARKMONITOR_EXTENSION_DEFINITION_ID')),
                                                       name=str(
                                                           os.getenv('MARKMONITOR_EXTENSION_DEFINITION_NAME')),
                                                       schema=str(
                                                           os.getenv('MARKMONITOR_EXTENSION_DEFINITION_SCHEMA')),
                                                       version='1',
                                                       created_by_ref=str(
                                                           os.getenv(
                                                               'MARKMONITOR_EXTENSION_DEFINITION_CREATE_BY')),
                                                       extension_types=['property-extension'],
                                                       created=datetime.strptime(os.getenv(
                                                           'MARKMONITOR_EXTENSION_DEFINITION_CREATE_DATE'),
                                                           '%Y-%m-%d'),
                                                       modified=datetime.strptime(os.getenv(
                                                           'MARKMONITOR_EXTENSION_DEFINITION_MODIFY_DATE'),
                                                           '%Y-%m-%d')
                                                       )

iana_extension_definition = ExtensionDefinition(id=str(os.getenv('IANA_EXTENSION_DEFINITION_ID')),
                                                name=str(
                                                    os.getenv('IANA_EXTENSION_DEFINITION_NAME')),
                                                schema=str(
                                                    os.getenv('IANA_EXTENSION_DEFINITION_SCHEMA')),
                                                version='1',
                                                created_by_ref=str(
                                                    os.getenv(
                                                        'IANA_EXTENSION_DEFINITION_CREATE_BY')),
                                                extension_types=['property-extension'],
                                                created=datetime.strptime(os.getenv(
                                                    'IANA_EXTENSION_DEFINITION_CREATE_DATE'),
                                                    '%Y-%m-%d'),
                                                modified=datetime.strptime(os.getenv(
                                                    'IANA_EXTENSION_DEFINITION_MODIFY_DATE'),
                                                    '%Y-%m-%d')
                                                )
tip_extension_definition = ExtensionDefinition(id=str(os.getenv('TIP_EXTENSION_DEFINITION_ID')),
                                               name=str(
                                                    os.getenv('TIP_EXTENSION_DEFINITION_NAME')),
                                               schema=str(
                                                    os.getenv('TIP_EXTENSION_DEFINITION_SCHEMA')),
                                               version='1',
                                               created_by_ref=str(
                                                    os.getenv(
                                                        'TIP_EXTENSION_DEFINITION_CREATE_BY')),
                                               extension_types=['property-extension'],
                                               created=datetime.strptime(os.getenv(
                                                    'TIP_EXTENSION_DEFINITION_CREATE_DATE'),
                                                    '%Y-%m-%d'),
                                               modified=datetime.strptime(os.getenv(
                                                    'TIP_EXTENSION_DEFINITION_MODIFY_DATE'),
                                                    '%Y-%m-%d')
                                               )
