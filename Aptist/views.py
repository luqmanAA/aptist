from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')


def handler404(request, exception):
    return render(request, '404.html')


def handler500(request):
    return render(request, '500.html')