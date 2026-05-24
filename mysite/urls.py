from django.contrib import admin
from django.urls import path, include
from .views import *  # jeśli w tym samym katalogu
from api import views as apiviews
urlpatterns = [
    path('', index),
    path('section/<str:dzial>', section),
    path('admin/', admin.site.urls),
    path('submitpost/', submitpost),
    path('post/<int:post_id>', post),
    path('submitreply/<int:post_id>', submitreply),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', register),
    path('post/<int:post_id>/favourite/', toggle_favourite, name='toggle_favourite'),
    path('favourites/', favourite_list, name='favourite_list'),
    path('api/section', apiviews.section),
    path('api/post', apiviews.post),
    path('api/reply', apiviews.reply),
    path('api/image/<int:imageid>', apiviews.image)
]