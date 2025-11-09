from django.urls import path
from .views import MaliciousFileView, get_list

urlpatterns = [
    path('', MaliciousFileView.as_view(), name='malicious_file_view'),
    path('list', get_list, name='get_list'),
]