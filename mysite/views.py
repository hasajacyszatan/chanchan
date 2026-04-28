from posty.models import Post
from posty.models import *
from django.shortcuts import render as django_render
from django.shortcuts import redirect
def render(request, template_name, context=None):
    if context is None:
        context = {}

    context['sections'] = Section.objects.all()
    return django_render(request, template_name, context)

def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})
def section(request, dzial):
    section = Section.objects.get(name=dzial)
    posts = Post.objects.filter(section=section.id)
    return render(request, 'index.html', {'posts': posts, "section": section})
def submitpost(request):
    print(request.FILES)
    uploaded_file = request.FILES.get('file')
    title = request.POST.get("title")
    content = request.POST.get("content")
    section_id = request.POST.get("section_id")
    section = Section.objects.get(id=section_id)
    newpost = Post(title = title, content = content, section = section)
    newpost.save()
    if uploaded_file:
        print("dostano plik")
        with open(f"static/images/{uploaded_file.name}", "wb+") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        image = Image(image_path = '/static/images/'+uploaded_file.name, post = newpost)
        image.save()
    return redirect('/')
def submitreply(request, post_id):
    post = Post.objects.filter(id=post_id)[0]
    content = request.POST.get("content")
    uploaded_file = request.FILES.get('file')
    newreply = Reply(content = content, reply_to = post)
    newreply.save()
    if uploaded_file:
        print("dostano plik")
        with open(f"static/images/{uploaded_file.name}", "wb+") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        image = Image(image_path = '/static/images/'+uploaded_file.name, reply = newreply)
        image.save()
    return redirect('/post/'+str(post_id))
def post(request, post_id):
    posts = Post.objects.filter(id=post_id)
    return render(request, 'post.html', {'posts': posts})