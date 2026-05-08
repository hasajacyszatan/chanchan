from django.contrib import admin
from django.urls import path, include
from .views import *  # jeśli w tym samym katalogu

urlpatterns = [
    path('', index),
    path('section/<str:dzial>', section),
    path('admin/', admin.site.urls),
    path('submitpost/', submitpost),
    path('post/<int:post_id>', post),
    path('submitreply/<int:post_id>', submitreply),
    path('accounts/', include('django.contrib.auth.urls')),
]