from django.urls import path

from tag.view.views import get_list, tag_view, get_category

urlpatterns = [
    path('', tag_view.as_view(), name='tag_view'),
    path('list', get_list, name='get_list'),
    path('category', get_category, name='get_category'),
]
