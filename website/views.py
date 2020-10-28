""""""
from django.http import HttpResponse


def root_index(request):

    return HttpResponse(request, 'index.html')
