from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST

from main.models import Experience, GalleryItem, Highlight, Project
from main.forms import ProjectForm, HighlightForm,ExperienceForm, GalleryItemForm
import datetime

OWNER_NAME = "Danar Iqbal Abi Zaidan Suharso"
EDITOR_GROUP_NAME = "Editor"


def is_editor(user):
    return user.is_authenticated and user.groups.filter(name=EDITOR_GROUP_NAME).exists()


def can_edit_portfolio(user):
    return user.is_superuser or is_editor(user)


def can_create_or_delete_portfolio(user):
    return user.is_superuser


def portfolio_permissions(user):
    return {
        "can_create_portfolio": can_create_or_delete_portfolio(user),
        "can_edit_portfolio": can_edit_portfolio(user),
        "can_delete_portfolio": can_create_or_delete_portfolio(user),
    }


def show_main(request):
    last_login = request.COOKIES.get(
    "last_login",
    "Belum ada sesi login / Cookie tidak ditemukan"
    )
    context = {
        "name": OWNER_NAME,
        "npm": "2506534371",
        "study_program": "S1 Sistem Informasi",
        "bio":"Passionate about developments in the IT and business sectors. ",
        "experience_list": Experience.objects.all(),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    json_response = get_experiences_json(request)

    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [experience.object for experience in experiences]

    context = {
        "name": OWNER_NAME,
        "experience_list": experiences,
        **portfolio_permissions(request.user),
    }
    return render(request, "experience.html", context)

def get_experiences_json(request):
    experiences = Experience.objects.all()
    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")


@login_required(login_url="/login/")
def create_experience(request):
    if not can_create_or_delete_portfolio(request.user):
        raise PermissionDenied

    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Danar",
        "form": form,
        "is_edit": False,
    }
    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not can_edit_portfolio(request.user):
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Danar",
        "form": form,
        "is_edit": True,
        "experience": experience,
    }
    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not can_create_or_delete_portfolio(request.user):
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")


def show_highlights(request):
    json_response = get_highlights_json(request)

    highlights = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    highlights = [highlight.object for highlight in highlights]

    context = {
        "name": OWNER_NAME,
        "highlights": highlights,
        **portfolio_permissions(request.user),
    }
    return render(request, "highlights.html", context)

def get_highlights_json(request):
    highlights = Highlight.objects.all().order_by("-year", "title")
    highlights_json = serializers.serialize("json", highlights)
    return HttpResponse(highlights_json, content_type="application/json")


@login_required(login_url="/login/")
def create_highlight(request):
    if not can_create_or_delete_portfolio(request.user):
        raise PermissionDenied

    form = HighlightForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Highlight baru berhasil ditambahkan!")
        return redirect("main:show_highlights")

    context = {
        "name": "Danar",
        "form": form,
        "is_edit": False,
    }
    return render(request, "highlights_form.html", context)


@login_required(login_url="/login/")
def update_highlight(request, highlight_id):
    if not can_edit_portfolio(request.user):
        raise PermissionDenied

    highlight = get_object_or_404(Highlight, pk=highlight_id)
    form = HighlightForm(request.POST or None, instance=highlight)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Highlight berhasil diperbarui!")
        return redirect("main:show_highlights")

    context = {
        "name": "Danar",
        "form": form,
        "is_edit": True,
        "highlight": highlight,
    }
    return render(request, "highlights_form.html", context)


@login_required(login_url="/login/")
def delete_highlight(request, highlight_id):
    if not can_create_or_delete_portfolio(request.user):
        raise PermissionDenied

    highlight = get_object_or_404(Highlight, pk=highlight_id)

    if request.method == "POST":
        highlight.delete()
        messages.success(request, "Highlight berhasil dihapus!")
        return redirect("main:show_highlights")

    return redirect("main:show_highlights")


def show_gallery(request):
    context = {
        "name": OWNER_NAME,
        "title_query": request.GET.get("title", "").strip(),
        "form": GalleryItemForm(),
        **portfolio_permissions(request.user),
    }
    return render(request, "gallery.html", context)


def get_gallery_items_json(request):
    title_query = request.GET.get("title", "").strip()
    gallery_items = GalleryItem.objects.prefetch_related("starred_by").all().order_by("-featured", "-year", "title")

    if title_query:
        gallery_items = gallery_items.filter(title__icontains=title_query)

    data = []
    for item in gallery_items:
        starred_users = item.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([user.username for user in starred_users])

        data.append({
            "pk": item.id,
            "fields": {
                "title": item.title,
                "caption": item.caption,
                "category": item.category,
                "location": item.location,
                "year": item.year,
                "image": item.image,
                "featured": item.featured,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            },
        })

    return JsonResponse(data, safe=False)


@login_required(login_url="/login/")
def create_gallery_item(request):
    if not can_create_or_delete_portfolio(request.user):
        raise PermissionDenied

    form = GalleryItemForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Foto baru berhasil ditambahkan!")
        return redirect("main:show_gallery")

    context = {
        "name": "Danar Iqbal Abi Zaidan Suharso",
        "form": form,
        "is_edit": False,
    }
    return render(request, "gallery_form.html", context)


@login_required(login_url="/login/")
def update_gallery_item(request, item_id):
    if not can_edit_portfolio(request.user):
        raise PermissionDenied

    item = get_object_or_404(GalleryItem, pk=item_id)
    form = GalleryItemForm(request.POST or None, instance=item)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Foto berhasil diperbarui!")
        return redirect("main:show_gallery")

    context = {
        "name": "Danar",
        "form": form,
        "is_edit": True,
        "item": item,
    }
    return render(request, "gallery_form.html", context)


@login_required(login_url="/login/")
def delete_gallery_item(request, item_id):
    if not can_create_or_delete_portfolio(request.user):
        raise PermissionDenied

    item = get_object_or_404(GalleryItem, pk=item_id)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Foto berhasil dihapus!")
        return redirect("main:show_gallery")

    return redirect("main:show_gallery")


@login_required(login_url="/login/")
def toggle_gallery_star(request, item_id):
    item = get_object_or_404(GalleryItem, pk=item_id)

    if request.method == "POST":
        if request.user in item.starred_by.all():
            item.starred_by.remove(request.user)
        else:
            item.starred_by.add(request.user)

    return redirect("main:show_gallery")


@require_POST
def create_gallery_item_ajax(request):
    if not can_create_or_delete_portfolio(request.user):
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan foto."},
            status=403,
        )

    form = GalleryItemForm(request.POST)
    if form.is_valid():
        item = form.save()
        return JsonResponse(
            {"message": "Foto berhasil ditambahkan.", "pk": item.id},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@login_required(login_url="/login/")
def create_project(request):
    if not can_create_or_delete_portfolio(request.user):
        raise PermissionDenied
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Danar",
        "form": form,
        "is_edit": False,
    }
    return render(request, "projects_form.html", context)


@login_required(login_url="/login/")
def update_project(request, project_id):
    if not can_edit_portfolio(request.user):
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Project berhasil diperbarui!")
        return redirect("main:show_projects")

    context = {
        "name": "Danar",
        "form": form,
        "is_edit": True,
        "project": project,
    }
    return render(request, "projects_form.html", context)


def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": OWNER_NAME,
        "title_query": title_query,
        "form": ProjectForm(),
        **portfolio_permissions(request.user),
    }
    return render(request, "projects.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "project_url": project.project_url,
                "project_image_url": project.project_image_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not can_create_or_delete_portfolio(request.user):
        raise PermissionDenied
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")


def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": OWNER_NAME,
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie("last_login", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return response

    context = {
        "name": OWNER_NAME,
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response

# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star
@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")

@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)
