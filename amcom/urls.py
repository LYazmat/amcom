from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stationery.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]
