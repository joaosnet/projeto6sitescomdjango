# url - view - template

from django.urls import path, include # new
from .views import homepage # new

urlpatterns = [
    path('', homepage), # new
] 