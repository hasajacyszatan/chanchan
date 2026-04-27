from posty.models import Post
from posty.models import Section
from django.shortcuts import render as django_render

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
    print(posts[0].images)
    return render(request, 'index.html', {'posts': posts})