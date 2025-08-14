"""
Simple URL configuration for tests
"""
from django.urls import path
from django.http import HttpResponse

def test_view(request):
    return HttpResponse("Test view")

urlpatterns = [
    path('test/', test_view, name='test'),
]
