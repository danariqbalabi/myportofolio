from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, request
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required  # Tambahkan baris ini
from django.core.exceptions import PermissionDenied        # Tambahkan baris ini

from main.models import Experience, GalleryItem, Highlight, Project
from main.forms import ProjectForm, HighlightForm,ExperienceForm, GalleryItemForm
import datetime

def show_main(request):
    last_login = request.COOKIES.get(
    "last_login",
    "Belum ada sesi login / Cookie tidak ditemukan"
    )
    context = {
        "name": "Danar Iqbal Abi Zaidan Suharso",
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
        "name": "Danar Iqbal Abi Zaidan Suharso",
        "experience_list": experiences,
    }
    return render(request, "experience.html", context)

def get_experiences_json(request):
    experiences = Experience.objects.all()
    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")


def create_experience(request):
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


def update_experience(request, experience_id):
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


def delete_experience(request, experience_id):
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
        "name": "Danar Iqbal Abi Zaidan Suharso",
        "highlights": highlights,
    }
    return render(request, "highlights.html", context)

def get_highlights_json(request):
    highlights = Highlight.objects.all().order_by("-year", "title")
    highlights_json = serializers.serialize("json", highlights)
    return HttpResponse(highlights_json, content_type="application/json")


def create_highlight(request):
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


def update_highlight(request, highlight_id):
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


def delete_highlight(request, highlight_id):
    highlight = get_object_or_404(Highlight, pk=highlight_id)

    if request.method == "POST":
        highlight.delete()
        messages.success(request, "Highlight berhasil dihapus!")
        return redirect("main:show_highlights")

    return redirect("main:show_highlights")


def show_gallery(request):
    json_response = get_gallery_items_json(request)

    gallery_items = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    gallery_items = [item.object for item in gallery_items]

    context = {
        "name": "Danar Iqbal Abi Zaidan Suharso",
        "gallery_items": gallery_items,
    }
    return render(request, "gallery.html", context)


def get_gallery_items_json(request):
    gallery_items = GalleryItem.objects.all().order_by("-featured", "-year")
    gallery_items_json = serializers.serialize("json", gallery_items)
    return HttpResponse(gallery_items_json, content_type="application/json")


def create_gallery_item(request):
    form = GalleryItemForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Foto baru berhasil ditambahkan!")
        return redirect("main:show_gallery")

    context = {
        "name": "Danar",
        "form": form,
        "is_edit": False,
    }
    return render(request, "gallery_form.html", context)


def update_gallery_item(request, item_id):
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


def delete_gallery_item(request, item_id):
    item = get_object_or_404(GalleryItem, pk=item_id)

    if request.method == "POST":
        item.delete()
        messages.success(request, "Foto berhasil dihapus!")
        return redirect("main:show_gallery")

    return redirect("main:show_gallery")

@login_required(login_url="/login/")  # Tambahkan baris ini
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Danar",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Danar",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    serializers.serialize("json", projects, use_natural_foreign_keys=True)
    return HttpResponse(projects_json, content_type="application/json")

@login_required(login_url="/login/")  # Tambahkan baris ini
def delete_project(request, project_id):
    if not request.user.is_superuser:
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
        "name": "Danar Iqbal Abi Zaidan Suharso",
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
        "name": "Danar Iqbal Abi Zaidan Suharso",
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