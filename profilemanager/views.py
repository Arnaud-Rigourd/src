from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("<h1>Hello, world. You're at the profilemanager index.</h1>")
