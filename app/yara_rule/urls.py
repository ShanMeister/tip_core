from django.urls import path
from .views import get_html, get_new_yara_html, YaraRuleView, generate_uuid, get_name, get_list

urlpatterns = [
    path('', get_html, name='get_html'),
    path('update/', get_new_yara_html, name='get_new_yara_html'),
    path('view/', YaraRuleView.as_view(), name='view'),
    path('generate_uuid/', generate_uuid, name='generate_uuid'),
    path('name/', get_name, name='get_name'),
    path('list/', get_list, name='get_list'),
    # path('tag/', get_tag, name='get_tag'),
    # path('members/<str:pk>/', MemberDetailView.as_view(), name='member_detail'),
]