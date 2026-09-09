from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Danar Iqbal Abi Zaidan Suharso",
        "npm": "2506534371",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Passionate about developments in the IT and business sectors. "
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Danar Iqbal Abi Zaidan Suharso",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)