""""""
from django.shortcuts import render


def root_index(request):

    return render(request, 'index.html')