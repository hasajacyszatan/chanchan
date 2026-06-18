from posty.models import *
from django.http import HttpResponse
from django.shortcuts import render as django_render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from PIL import Image as PILImage
import math
import uuid
import os


# ── Helpers ───────────────────────────────────────────────────────────────────

def render(request, template_name, context=None):
    """Wrapper dodający sections do każdego kontekstu."""
    if context is None:
        context = {}
    context['sections'] = Section.objects.all()
    return django_render(request, template_name, context)


def save_uploaded_image(uploaded_file, related_obj, relation_type="post"):
    """
    Zapisuje przesłany obraz (pełny + miniatura).
    Zwraca obiekt Image lub rzuca ValueError gdy plik za duży.
    """
    MAX_SIZE = 4 * 1024 * 1024
    if uploaded_file.size > MAX_SIZE:
        raise ValueError(f'Plik "{uploaded_file.name}" jest za duży (max 4 MB).')

    filename = str(uuid.uuid4())
    img = PILImage.open(uploaded_file)

    # Konwersja do RGB żeby JPEG/PNG z kanałem alpha nie sypał błędami
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")

    full_path      = f"static/images/{filename}.png"
    thumbnail_path = f"static/images/{filename}_thumbnail.png"

    img.save(full_path)
    img.thumbnail((300, 300))
    img.save(thumbnail_path)

    image_data = {
        "image_path":           "/" + full_path,
        "thumbnail_image_path": "/" + thumbnail_path,
    }
    if relation_type == "post":
        image_data["post"] = related_obj
    else:
        image_data["reply"] = related_obj

    image = Image(**image_data)
    image.save()
    return image


def _save_images_from_request(request, related_obj, relation_type="post"):
    """
    Pobiera wszystkie pliki o nazwach file, file2, file3, … z request.FILES
    i zapisuje je. Zwraca HttpResponse z błędem albo None gdy OK.
    """
    # Zbieramy pliki w kolejności: file, file2, file3, ...
    files = []
    for key in sorted(request.FILES.keys()):
        if key == 'file' or (key.startswith('file') and key[4:].isdigit()):
            files.append(request.FILES[key])

    for uploaded_file in files:
        try:
            save_uploaded_image(uploaded_file, related_obj, relation_type)
        except ValueError as e:
            return HttpResponse(str(e), status=400)
    return None


# ── Widoki ────────────────────────────────────────────────────────────────────

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
    POSTS_PER_PAGE = 5
    section = get_object_or_404(Section, name=dzial)
    qs = Post.objects.filter(section=section).order_by('-id')

    page = max(int(request.GET.get("page", 0)), 0)
    pagecount = math.ceil(qs.count() / POSTS_PER_PAGE)
    posts = qs[POSTS_PER_PAGE * page : POSTS_PER_PAGE * (page + 1)]

    return render(request, 'section.html', {
        'posts':     posts,
        'section':   section,
        'pagecount': range(pagecount),
        'current_page': page,
    })


def submitpost(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    title      = request.POST.get("title", "").strip()
    content    = request.POST.get("content", "").strip()
    section_id = request.POST.get("section_id")
    section    = get_object_or_404(Section, id=section_id)

    # Używamy request.user zamiast ufać danym z POST
    user = request.user if request.user.is_authenticated else None

    newpost = Post(title=title, content=content, section=section, user=user)
    newpost.save()

    err = _save_images_from_request(request, newpost, "post")
    if err:
        return err

    return redirect('/section/' + section.name)


def submitreply(request, post_id):
    if request.method != "POST":
        return HttpResponse(status=405)

    post    = get_object_or_404(Post, id=post_id)
    content = request.POST.get("content", "").strip()
    user = request.user if request.user.is_authenticated else None
    newreply = Reply(content=content, reply_to=post, user=user)
    newreply.save()

    err = _save_images_from_request(request, newreply, "reply")
    if err:
        return err

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
    return redirect('favourite_list')


@login_required
def favourite_list(request):
    fav_posts = request.user.favourite_posts.all()
    return render(request, 'favourites.html', {'posts': fav_posts})


# ── Profil użytkownika ────────────────────────────────────────────────────────────────────
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, _ = UserProfile.objects.get_or_create(user=profile_user)
    user_posts = Post.objects.filter(user=profile_user).order_by('-id')
    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'user_posts': user_posts,
    })

@login_required
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.bio = request.POST.get('bio', '').strip()[:500]

        if 'avatar' in request.FILES:
            uploaded = request.FILES['avatar']
            if uploaded.size > 4 * 1024 * 1024:
                return render(request, 'edit_profile.html', { 'profile': profile,  'error':    'Plik jest za duży (max 4MB).',
                })
            try:
                filename = str(uuid.uuid4())
                img = PILImage.open(uploaded)
                if img.mode not in ("RGB", "L"):
                    img = img.convert("RGB")
                w, h = img.size
                min_dim = min(w, h)
                img = img.crop(((w - min_dim) // 2, (h - min_dim) // 2,
                                   (w + min_dim) // 2, (h + min_dim) // 2))
                img = img.resize((200, 200), PILImage.LANCZOS)
                avatar_dir = "static/images/avatars"
                os.makedirs(avatar_dir, exist_ok=True)
                path = f"{avatar_dir}/{filename}.png"
                img.save(path)
                profile.avatar_path = "/" + path
            except Exception as e:
                return render(request, 'edit_profile.html', {'profile': profile,'error': f'Błąd przetwarzania obrazu: {e}',
                })
            
        profile.save()
        return redirect('user_profile', username=request.user.username)
        
    return render(request, 'edit_profile.html', {'profile': profile})

@login_required
def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    if reply.user == request.user or request.user.is_staff or reply.reply_to.user == request.user:
        reply.delete()
        
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    section_name = post.section.name
    if post.user == request.user or request.user.is_staff:
        post.delete()
        referer = request.META.get('HTTP_REFERER', '')
        if f'/post/{post_id}' in referer:
            return redirect(f'/section/{section_name}')
            
    return redirect(request.META.get('HTTP_REFERER', '/'))