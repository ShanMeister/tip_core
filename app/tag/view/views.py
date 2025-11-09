import dataclasses
import json
import logging

from dacite import from_dict, MissingValueError
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from common.error.response_message_enum import APIResponseEnum
from app.tag.entity.tag import Tag
from app.tag.repository.tag_repository_elastic import TagRepository
from app.tag.use_case.dto.delete_tag_dto import DeleteTagDto
from app.tag.use_case.dto.get_tag_search import TagSearch
from app.tag.use_case.tag_service import TagService

logger = logging.getLogger(__name__)
tag_service_object = TagService(TagRepository())


class tag_view(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'label_management.html')

    def post(self, request, *args, **kwargs):
        try:
            tag = from_dict(data_class=Tag, data=json.loads(request.body))
            tag_service_object.save_tag(tag)
        except ValueError:
            return JsonResponse({'status': APIResponseEnum.FAIL.value, 'message': '已存在tag標籤'}, status=400)
        except MissingValueError as e:
            logger.error(e, exc_info=1)
            return JsonResponse({'status': APIResponseEnum.FAIL.value, 'message': '請輸入必填標籤與分類'}, status=400)
        except Exception as e:
            logger.error(e, exc_info=1)
            return JsonResponse(
                {'status': APIResponseEnum.FAIL.value, 'message': APIResponseEnum.INTERNAL_SERVER_ERROR.value},
                status=500)

        return JsonResponse({'status': APIResponseEnum.SUCCESS.value}, status=200)

    def delete(self, request, *args, **kwargs):
        try:
            delete_tag = from_dict(data_class=DeleteTagDto, data=json.loads(request.body))
            if delete_tag.id is None:
                return JsonResponse({'status': APIResponseEnum.FAIL.value}, status=400)

            tag_service_object.delete_tag(delete_tag)
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
            tag_search = TagSearch(search_text=query_dict['search']['search_text'],
                                   category=query_dict['search']['category'],
                                   current_page=query_dict['paging']['current_page'],
                                   page_size=query_dict['paging']['page_size'])
            return JsonResponse(dataclasses.asdict(tag_service_object.get_paging(tag_search)))
        except Exception as e:
            logger.error(e, exc_info=1)
            return JsonResponse(
                {'status': APIResponseEnum.FAIL.value, 'message': APIResponseEnum.INTERNAL_SERVER_ERROR.value},
                status=500)


def get_category(request):
    if request.method == 'GET':
        try:
            category_list_dict = {
                'category': [item.category for item in tag_service_object.get_tag_category()]
            }
            return JsonResponse(category_list_dict)
        except Exception as e:
            logger.error(e, exc_info=1)
            return JsonResponse(
                {'status': APIResponseEnum.FAIL.value, 'message': APIResponseEnum.INTERNAL_SERVER_ERROR.value},
                status=500)
