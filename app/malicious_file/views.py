import json
import uuid
import logging
import dataclasses

from dacite import from_dict, MissingValueError
from common.error.response_message_enum import APIResponseEnum
from django.http import JsonResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.views import View

from app.malicious_file.use_case.use_case import MaliciousFileUseCase
from app.malicious_file.repository import MaliciousFileRepository
from app.malicious_file.use_case.dto.get_file_search import FileSearch
from app.malicious_file.use_case.dto.delete_file_dto import DeleteFileDto

logger = logging.getLogger(__name__)
malicious_file_service_object = MaliciousFileUseCase(MaliciousFileRepository())


class MaliciousFileView(View):

    def get(self, request):
        return render(request, 'malicious_file.html')

    def post(self, request):
        try:
            data = json.loads(request.body)
            malicious_file_service_object.save_file(data)
            return JsonResponse({'message': 'Malicious file saved successfully'})
        except ValueError:
            return JsonResponse({'status': APIResponseEnum.FAIL.value, 'message': '已存在 malicious file'}, status=400)
        except MissingValueError as e:
            return JsonResponse({'status': APIResponseEnum.FAIL.value, 'message': '請輸入必填檔案、名稱與內容'},
                                status=400)
        except Exception as e:
            return JsonResponse(
                {'status': APIResponseEnum.FAIL.value, 'message': APIResponseEnum.INTERNAL_SERVER_ERROR.value},
                status=500)

    def delete(self, request):
        try:
            delete_file = from_dict(data_class=DeleteFileDto, data=json.loads(request.body))
            if delete_file.id is None:
                return JsonResponse({'status': APIResponseEnum.FAIL.value}, status=400)

            malicious_file_service_object.delete_file(delete_file)
        except Exception as e:
            logger.error(e, exc_info=1)
            return JsonResponse(
                {'status': APIResponseEnum.FAIL.value, 'message': APIResponseEnum.INTERNAL_SERVER_ERROR.value},
                status=500)

        return JsonResponse({'status': APIResponseEnum.SUCCESS.value}, status=200)


def get_list(request):
    if request.method == 'SEARCH':
        try:
            query_dict = json.loads(request.body)
            tag_search = FileSearch(search_text=query_dict['search']['search_text'],
                                    category=query_dict['search']['category'],
                                    current_page=query_dict['paging']['current_page'],
                                    page_size=query_dict['paging']['page_size'])
            return JsonResponse(dataclasses.asdict(malicious_file_service_object.get_paging(tag_search)))
        except Exception as e:
            logger.error(e, exc_info=1)
            return JsonResponse(
                {'status': APIResponseEnum.FAIL.value, 'message': APIResponseEnum.INTERNAL_SERVER_ERROR.value},
                status=500)
