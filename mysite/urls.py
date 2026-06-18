from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import *  # jeśli w tym samym katalogu
from api import views as apiviews
from posty.views import regulamin
from . import views
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
    path('api/image/<int:imageid>', apiviews.image),
    path('regulamin/', regulamin, name='regulamin'),
    path('tworcy/', TemplateView.as_view(template_name='tworcy.html'), name='tworcy'),
    path('user/<str:username>/',    profile_view, name='user_profile'),
    path('profile/edit/',   edit_profile, name='edit_profile'),
    path('delete-reply/<int:reply_id>/', views.delete_reply, name='delete_reply'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
]