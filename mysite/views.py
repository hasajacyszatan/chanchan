from django.shortcuts import render
from posty.models import Post
from posty.models import Section
def index(request):
    posts = Post.objects.all()
    sections = Section.objects.all()
    return render(request, 'index.html', {'posts': posts, 'sections': sections})
def section(request, dzial):
    sections = Section.objects.all()
    section = Section.objects.get(name=dzial)
    posts = Post.objects.filter(section=section.id)
    print(dir(posts[0]))
    return render(request, 'index.html', {'posts': posts, 'sections': sections})