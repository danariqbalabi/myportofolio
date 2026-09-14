from django.shortcuts import render

from main.models import Experience, Highlight


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
    context = {
        "name": "Danar Iqbal Abi Zaidan Suharso",
        "highlights": Highlight.objects.all().order_by("-year", "title"),
    }
    return render(request, "highlights.html", context)
