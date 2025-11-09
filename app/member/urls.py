from django.urls import path

from member.views import get_members

urlpatterns = [
    path('', get_members, name='get_member'),
]