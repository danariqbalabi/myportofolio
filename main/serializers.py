from django.utils.html import strip_tags
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import URLValidator
from rest_framework import serializers

from .models import GalleryItem, Project


class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "tech_stack", "project_url",
            "project_image_url", "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Judul tidak boleh kosong.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_tech_stack(self, value):
        return strip_tags(value)

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        return bool(request and request.user.is_authenticated and request.user in obj.starred_by.all())

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class GalleryItemSerializer(ProjectSerializer):
    class Meta:
        model = GalleryItem
        fields = ["id", "title", "caption", "category", "location", "year", "image", "featured",
                  "star_count", "is_starred", "starred_by_names"]
        read_only_fields = ["id"]

    def validate_caption(self, value):
        return strip_tags(value).strip()

    def validate_category(self, value):
        return strip_tags(value).strip()

    def validate_location(self, value):
        return strip_tags(value).strip()

    def validate_image(self, value):
        # Existing gallery data uses /static/img/... as well as external URLs.
        if value.startswith("/static/") and ".." not in value and "\\" not in value:
            return value
        try:
            URLValidator(schemes=["http", "https"])(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Gunakan URL HTTP/HTTPS atau gambar di /static/.")
        return value

    def validate_year(self, value):
        if not 2000 <= value <= 2100:
            raise serializers.ValidationError("Tahun harus di antara 2000 dan 2100.")
        return value
