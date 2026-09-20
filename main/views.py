from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience, GalleryItem, Highlight, Project
from main.forms import ProjectForm, HighlightForm

def show_main(request):
    context = {
        "name": "Danar Iqbal Abi Zaidan Suharso",
        "npm": "2506534371",
        "study_program": "S1 Sistem Informasi",
        "bio":"Passionate about developments in the IT and business sectors. ",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Danar Iqbal Abi Zaidan Suharso",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


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
    context = {
        "name": "Danar Iqbal Abi Zaidan Suharso",
        "gallery_items": GalleryItem.objects.all().order_by("-featured", "-year"),
    }
    return render(request, "gallery.html", context)

def create_project(request):
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

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")