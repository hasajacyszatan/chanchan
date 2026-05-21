from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Post

@login_required
def toggle_favourite(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def favourite_list(request):
    fav_posts = request.user.favourite_posts.all()
    return render(request, 'favourites.html', {'posts': fav_posts})

# Create your views here.