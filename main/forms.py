from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Textarea, URLInput, NumberInput, Select, CheckboxInput
from django.utils.html import strip_tags

from main.models import Project, Highlight, GalleryItem, Experience

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_tech_stack(self):
        return strip_tags(self.cleaned_data["tech_stack"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

class HighlightForm(ModelForm):
    class Meta:
        model = Highlight
        fields = [
            "title",
            "description",
            "category",
            "year",
            "thumbnail",
        ]

        labels = {
            "title": "Judul Highlight",
            "description": "Deskripsi",
            "category": "Kategori",
            "year": "Tahun",
            "thumbnail": "URL Gambar",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Juara 1 RISTEK Datathon 2026",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pencapaianmu",
                    "rows": 3,
                }
            ),
            "category": TextInput(
                attrs={
                    "placeholder": "Competition, Organization, Academic, dll",
                    "maxlength": 100,
                }
            ),
            "year": NumberInput(
                attrs={
                    "placeholder": "2026",
                    "min": 2000,
                    "max": 2100,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }
class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
        ]

        labels = {
            "title": "Nama Pengalaman",
            "description": "Deskripsi",
            "category": "Kategori",
            "thumbnail": "URL Gambar",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Backend Developer Intern",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pengalamanmu",
                    "rows": 3,
                }
            ),
            "category": Select(),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }


class GalleryItemForm(ModelForm):
    class Meta:
        model = GalleryItem
        fields = [
            "title",
            "caption",
            "category",
            "location",
            "year",
            "image",
            "featured",
        ]

        labels = {
            "title": "Judul",
            "caption": "Caption",
            "category": "Kategori",
            "location": "Lokasi",
            "year": "Tahun",
            "image": "URL Gambar",
            "featured": "Tampilkan sebagai Featured",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Sunrise at Kawah Ratu",
                    "maxlength": 255,
                }
            ),
            "caption": Textarea(
                attrs={
                    "placeholder": "Ceritakan momen ini",
                    "rows": 3,
                }
            ),
            "category": TextInput(
                attrs={
                    "placeholder": "Travel, Event, Hobby, dll",
                    "maxlength": 100,
                }
            ),
            "location": TextInput(
                attrs={
                    "placeholder": "Sukabumi, Jawa Barat",
                    "maxlength": 255,
                }
            ),
            "year": NumberInput(
                attrs={
                    "placeholder": "2026",
                    "min": 2000,
                    "max": 2100,
                }
            ),
            "image": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
            "featured": CheckboxInput(),
        }
