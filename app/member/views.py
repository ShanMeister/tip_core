from django.http import JsonResponse

from member.documents import MemberDocument


# Create your views here.
def get_members(request):

    return JsonResponse({'test': 'qweqweqwe'}, safe=False)
