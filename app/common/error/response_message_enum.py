from enum import Enum


class APIResponseEnum(Enum):
    INTERNAL_SERVER_ERROR = '內部出錯，請聯絡系統管理員'
    SUCCESS = 'OK'
    FAIL = 'fail'
