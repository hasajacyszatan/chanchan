from django.http import JsonResponse, FileResponse, Http404
from django.conf import settings
from posty.models import *
import os


def section(request):
    section_id = request.GET.get("id")
    section_name = request.GET.get("name")

    sections = Section.objects.all()

    if section_id:
        sections = sections.filter(id=section_id)

    if section_name:
        sections = sections.filter(name=section_name)

    data = list(
        sections.values("id", "name", "image_path", "description")
    )

    return JsonResponse(data, safe=False)


def post(request):
    post_id = request.GET.get("id")
    section_id = request.GET.get("section_id")

    posts = Post.objects.all()

    if post_id:
        posts = posts.filter(id=post_id)

    if section_id:
        posts = posts.filter(section_id=section_id)

    data = list(
        posts.values("id", "title", "images", "content", "section_id", "user")
    )

    return JsonResponse(data, safe=False)

def reply(request):
    reply_id = request.GET.get("id")
    post_id = request.GET.get("post_id")

    replies = Reply.objects.all()

    if reply_id:
        replies = replies.filter(id=reply_id)

    if post_id:
        replies = replies.filter(reply_to=post_id)

    data = list(
        replies.values(
            "id",
            "reply_to",
            "content",
            "created_at",
            "user"
        )
    )

    return JsonResponse(data, safe=False)

def image(request, imageid):
    try:
        image = Image.objects.get(id=imageid)
    except Image.DoesNotExist:
        raise Http404("Obraz nie istnieje.")

    # image_path to URL np. /media/images/uuid.png
    # Zamieniamy URL na ścieżkę dyskową
    relative = image.image_path.lstrip('/')           # media/images/uuid.png
    if relative.startswith(settings.MEDIA_URL.lstrip('/')):
        # Wytnij prefiks MEDIA_URL i sklej z MEDIA_ROOT
        rel_to_media = relative[len(settings.MEDIA_URL.lstrip('/')):]
        disk_path = os.path.join(settings.MEDIA_ROOT, rel_to_media)
    else:
        # Fallback — stara ścieżka zaczynająca się od static/
        disk_path = relative

    if not os.path.exists(disk_path):
        raise Http404("Plik obrazu nie istnieje na dysku.")

    return FileResponse(open(disk_path, "rb"), as_attachment=True)
