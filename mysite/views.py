from posty.models import *
from django.http import HttpResponse
from django.shortcuts import render as django_render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import os
import uuid
import math
from PIL import Image as PILImage
def save_uploaded_image(uploaded_file, verifyfile_func, related_obj, relation_type="post"):
    filename = str(uuid.uuid4())
    if not uploaded_file:
        return None

    if not verifyfile_func(uploaded_file):
        return "too_large"

    img = PILImage.open(uploaded_file)
    file_path = f"static/images/{filename}.png"
    img.save(file_path)
    thumbnail_file_path = f"static/images/{filename}_thumbnail.png"
    img.thumbnail((300,300))
    image_data = {
        "image_path": "/"+file_path,
        "thumbnail_image_path": "/"+thumbnail_file_path
    }
    img.save(thumbnail_file_path)
    if relation_type == "post":
        image_data["post"] = related_obj
    else:
        image_data["reply"] = related_obj

    image = Image(**image_data)
    image.save()

    return image
def verifyfile(value):
    limit = 4 * 1024 * 1024
    if value.size > limit:
        return False
    return True
def render(request, template_name, context=None):
    if context is None:
        context = {}

    context['sections'] = Section.objects.all()
    return django_render(request, template_name, context)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})
def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})
def section(request, dzial):
    postperpage = 5
    section = Section.objects.get(name=dzial)
    pagecount = math.ceil(len(Post.objects.filter(section=section.id).order_by('-id').all())/postperpage)
    page=int(request.GET.get("page",0))
    posts = Post.objects.filter(section=section.id).order_by('-id')[postperpage*page:(postperpage*page+postperpage)]
    return render(request, 'board.html', {'posts': posts, "section": section, "pagecount": range(pagecount)})
def submitpost(request):
    uploaded_file = request.FILES.get('file')
    title = request.POST.get("title")
    content = request.POST.get("content")
    section_id = request.POST.get("section_id")
    userid = request.POST.get("userid", None)
    print(userid)
    if not userid == "None":
        user = User.objects.get(id=userid)
    else:
        user = None
    section = Section.objects.get(id=section_id)

    newpost = Post(title=title, content=content, section=section, user=user)
    newpost.save()

    result = save_uploaded_image(uploaded_file, verifyfile, newpost, "post")

    if result == "too_large":
        return HttpResponse("zbyt duży plik")

    return redirect('/section/' + section.name)
def submitreply(request, post_id):
    post = Post.objects.get(id=post_id)
    content = request.POST.get("content")
    uploaded_file = request.FILES.get('file')

    newreply = Reply(content=content, reply_to=post)
    newreply.save()

    result = save_uploaded_image(uploaded_file, verifyfile, newreply, "reply")

    if result == "too_large":
        return HttpResponse("zbyt duży plik")

    return redirect('/post/' + str(post_id))
def post(request, post_id):
    posts = Post.objects.filter(id=post_id)
    return render(request, 'post.html', {'posts': posts})

@login_required
def toggle_favourite(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)

    return redirect('favourite_list', post_id=post.id)

@login_required
def favourite_list(request):
    fav_posts = request.user.favourite_posts.all()
    return render(request, 'favourites.html', {'posts': fav_posts})