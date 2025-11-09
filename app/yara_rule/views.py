import json
import uuid
import logging
import dataclasses

from dacite import MissingValueError
from common.error.response_message_enum import APIResponseEnum
from django.http import JsonResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.views import View

from app.yara_rule.use_case.use_case import YaraRuleUseCase
from app.yara_rule.repository import YaraRuleRepository
from app.yara_rule.use_case.dto.get_name_search import NameSearch

logger = logging.getLogger(__name__)
yara_rule_service_object = YaraRuleUseCase(YaraRuleRepository())


def get_html(request):
    return render(request, 'yara_rule/yara_rule_main.html')


def get_new_yara_html(request):
    return render(request, 'yara_rule/yara_rule_update.html')


def generate_uuid(request):
    new_uuid = uuid.uuid4()
    return JsonResponse({'uuid': str(new_uuid)})


class YaraRuleView(View):

    def get(self, request):
        try:
            data = yara_rule_service_object.fetch_all_yara_rules()
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def post(self, request):
        try:
            data = json.loads(request.body)
            yara_rule_service_object.save_yara_rule(data)
            return JsonResponse({'message': 'Yara rule saved successfully'})
        except ValueError:
            return JsonResponse({'status': APIResponseEnum.FAIL.value, 'message': '已存在yara rule'}, status=400)
        except MissingValueError as e:
            return JsonResponse({'status': APIResponseEnum.FAIL.value, 'message': '請輸入必填rule名稱與內容'}, status=400)
        except Exception as e:
            return JsonResponse(
                {'status': APIResponseEnum.FAIL.value, 'message': APIResponseEnum.INTERNAL_SERVER_ERROR.value},
                status=500)

    def delete(self, request):
        data = json.loads(request.body)
        rule_id = data['id']
        print(rule_id)
        try:
            yara_rule_service_object.delete_yara_rule(rule_id)
            return JsonResponse({'message': 'Yara rule deleted successfully'})
        except ObjectDoesNotExist:
            return JsonResponse({'status': APIResponseEnum.FAIL.value, 'message': 'Yara rule not found'}, status=404)
        except Exception as e:
            return JsonResponse(
                {'status': APIResponseEnum.FAIL.value, 'message': APIResponseEnum.INTERNAL_SERVER_ERROR.value},
                status=500)


def get_name(request):
    if request.method == 'GET':
        try:
            name_list_dict = {
                'name': [item.category for item in yara_rule_service_object.get_rule_name()]
            }
            return JsonResponse(name_list_dict)
        except Exception as e:
            logger.error(e, exc_info=1)
            return JsonResponse(
                {'status': APIResponseEnum.FAIL.value, 'message': APIResponseEnum.INTERNAL_SERVER_ERROR.value},
                status=500)


def get_list(request):
    if request.method == 'SEARCH':
        try:
            query_dict = json.loads(request.body)
            tag_search = NameSearch(search_text=query_dict['search']['search_text'],
                                    category=query_dict['search']['category'],
                                    current_page=query_dict['paging']['current_page'],
                                    page_size=query_dict['paging']['page_size'])
            return JsonResponse(dataclasses.asdict(yara_rule_service_object.get_paging(tag_search)))
        except Exception as e:
            logger.error(e, exc_info=1)
            return JsonResponse(
                {'status': APIResponseEnum.FAIL.value, 'message': APIResponseEnum.INTERNAL_SERVER_ERROR.value},
                status=500)
