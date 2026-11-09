from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from .models import GalleryItem, Project
from .serializers import GalleryItemSerializer, ProjectSerializer


class GalleryAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_superuser("owner", "owner@example.com", "test-password")
        cls.editor = User.objects.create_user("editor", password="test-password")
        cls.editor.groups.add(Group.objects.get_or_create(name="Editor")[0])
        cls.visitor = User.objects.create_user("visitor", password="test-password")
        cls.staff = User.objects.create_user("staff", password="test-password", is_staff=True)

    def setUp(self):
        GalleryItem.objects.all().delete()
        self.payload = {"title": "Sunrise", "caption": "Morning hike", "category": "Travel", "location": "Bogor",
                        "year": 2026, "image": "/static/img/kawah-ratu.jpeg", "featured": False}
        self.item = GalleryItem.objects.create(**self.payload)
        self.list_url = reverse("api:gallery-list")
        self.detail_url = reverse("api:gallery-detail", args=[self.item.pk])
        self.star_url = reverse("api:gallery-star", args=[self.item.pk])

    def test_public_read_search_head_options_and_missing(self):
        response = self.client.get(self.list_url, {"title": " SUN "})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["id"], self.item.pk)
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.list_url, {"title": "missing"}).data, [])
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)
        self.assertEqual(self.client.head(self.detail_url).content, b"")
        self.assertEqual(self.client.options(self.detail_url).status_code, 200)
        self.assertEqual(self.client.get(reverse("api:gallery-detail", args=[99999])).status_code, 404)
        self.assertEqual(GalleryItem.objects.count(), 1)

    def test_editor_can_patch_put_but_not_create_delete(self):
        self.client.force_authenticate(self.editor)
        self.assertEqual(self.client.patch(self.detail_url, {"title": "Updated"}, format="json").status_code, 200)
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, "Updated")
        self.assertEqual(self.item.caption, "Morning hike")
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 200)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(GalleryItem.objects.count(), 1)

    def test_guest_visitor_and_staff_cannot_manage(self):
        before = list(GalleryItem.objects.values())
        for user in (None, self.visitor, self.staff):
            self.client.force_authenticate(user)
            for method, url in [("post", self.list_url), ("put", self.detail_url),
                                ("patch", self.detail_url), ("delete", self.detail_url)]:
                with self.subTest(user=user, method=method):
                    payload = {**self.payload, "title": "Tidak boleh tersimpan", "featured": True}
                    self.assertEqual(getattr(self.client, method)(url, payload, format="json").status_code, 403)
                    self.assertEqual(list(GalleryItem.objects.values()), before)
                    self.assertEqual(self.item.starred_by.count(), 0)
        self.assertEqual(GalleryItem.objects.count(), 1)

    def test_owner_create_update_delete(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        url = reverse("api:gallery-detail", args=[response.data["id"]])
        self.assertEqual(self.client.put(url, {"title": "Incomplete"}, format="json").status_code, 400)
        self.assertEqual(self.client.patch(url, {"featured": True}, format="json").status_code, 200)
        self.assertTrue(GalleryItem.objects.get(pk=response.data["id"]).featured)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_validation_and_html_stripping(self):
        self.client.force_authenticate(self.owner)
        before = list(GalleryItem.objects.values())
        for field, value in [("title", "<b></b>"), ("image", "javascript:alert(1)"),
                             ("image", "data:text/html,x"), ("image", "/static/../secret"), ("year", 0)]:
            response = self.client.post(self.list_url, {**self.payload, field: value}, format="json")
            self.assertEqual(response.status_code, 400)
            self.assertIn(field, response.data)
            self.assertEqual(list(GalleryItem.objects.values()), before)
        response = self.client.post(self.list_url, {**self.payload, "title": "<b>Clean</b>",
            "caption": "<i>caption</i>", "image": "https://example.com/image.jpg"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "Clean")
        self.assertEqual(response.data["caption"], "caption")

    def test_invalid_patch_does_not_change_other_fields(self):
        self.client.force_authenticate(self.editor)
        before = list(GalleryItem.objects.values())
        response = self.client.patch(self.detail_url, {
            "title": '<img src="x" onerror="alert(1)">', "caption": "Jangan disimpan",
        }, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.data)
        self.assertEqual(list(GalleryItem.objects.values()), before)

    def test_gallery_text_fields_and_year_bounds(self):
        self.client.force_authenticate(self.owner)
        response = self.client.patch(self.detail_url, {
            "title": " <b>Foto baru</b> ", "caption": " <i>Caption</i> ",
            "category": " <b>Travel</b> ", "location": " <span>Bogor</span> ",
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, "Foto baru")
        self.assertEqual(self.item.caption, "Caption")
        self.assertEqual(self.item.category, "Travel")
        self.assertEqual(self.item.location, "Bogor")
        for year in (1999, 2101):
            with self.subTest(year=year):
                response = self.client.patch(self.detail_url, {"year": year}, format="json")
                self.assertEqual(response.status_code, 400)
                self.item.refresh_from_db()
                self.assertEqual(self.item.year, 2026)
        self.assertEqual(GalleryItemSerializer(self.item).data["is_starred"], False)

    def test_star_uses_session_user_and_computed_fields_read_only(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        for user in (self.visitor, self.editor):
            self.client.force_authenticate(user)
            response = self.client.post(self.star_url, {"user_id": self.owner.pk}, format="json")
            self.assertTrue(response.data["is_starred"])
            self.assertFalse(self.item.starred_by.filter(pk=self.owner.pk).exists())
            self.assertFalse(self.client.post(self.star_url).data["is_starred"])
        self.client.force_authenticate(self.owner)
        response = self.client.patch(self.detail_url, {"star_count": 99, "is_starred": True,
            "starred_by": [self.visitor.pk], "starred_by_names": "forged"}, format="json")
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertNotIn("email", response.data)
        self.assertNotIn("password", response.data)

    def test_real_session_csrf_for_update_delete_and_star(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="editor", password="test-password"))
        self.assertEqual(client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
        self.assertEqual(client.post(self.star_url).status_code, 403)
        client.get(reverse("main:show_gallery"))
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.patch(self.detail_url, {"title": "Changed"}, format="json", HTTP_X_CSRFTOKEN=token).status_code, 200)
        self.assertEqual(client.post(self.star_url, HTTP_X_CSRFTOKEN=token).status_code, 200)
        client.force_login(self.owner)
        self.assertEqual(client.delete(self.detail_url).status_code, 403)
        client.get(reverse("main:show_gallery"))
        self.assertEqual(client.delete(self.detail_url, HTTP_X_CSRFTOKEN=client.cookies["csrftoken"].value).status_code, 204)

    def test_bad_json_methods_and_permission_before_lookup(self):
        self.client.force_authenticate(self.owner)
        self.assertEqual(self.client.post(self.list_url, '{bad', content_type="application/json").status_code, 400)
        self.assertEqual(self.client.delete(self.list_url).status_code, 405)
        self.assertEqual(self.client.get(self.star_url).status_code, 405)
        self.client.force_authenticate(self.visitor)
        self.assertEqual(self.client.patch(reverse("api:gallery-detail", args=[99999]), {}, format="json").status_code, 403)


class ProjectSerializerTest(APITestCase):
    def test_serializer_without_request_and_prefetched_list(self):
        projects = [Project.objects.create(title=f"Project {i}", description="Description", tech_stack="Django") for i in range(4)]
        serializer = ProjectSerializer(projects[0])
        self.assertFalse(serializer.data["is_starred"])
        with self.assertNumQueries(2):
            data = ProjectSerializer(Project.objects.prefetch_related("starred_by"), many=True).data
            self.assertEqual(len(data), 4)
