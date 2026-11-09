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
        cls.visitor = User.objects.create_user("visitor", email="visitor@example.com", password="test-password")
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
        before = list(GalleryItem.objects.values())
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(list(GalleryItem.objects.values()), before)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(list(GalleryItem.objects.values()), before)

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
        self.assertEqual(self.item.starred_by.count(), 0)
        for user in (self.visitor, self.editor, self.owner):
            self.client.force_authenticate(user)
            response = self.client.post(self.star_url, {"user_id": self.staff.pk}, format="json")
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.data["is_starred"])
            self.assertEqual(list(self.item.starred_by.all()), [user])
            self.assertFalse(self.item.starred_by.filter(pk=self.staff.pk).exists())
            self.assertFalse(self.client.post(self.star_url).data["is_starred"])
            self.assertEqual(self.item.starred_by.count(), 0)
        self.client.force_authenticate(self.owner)
        response = self.client.patch(self.detail_url, {"star_count": 99, "is_starred": True,
            "starred_by": [self.visitor.pk], "starred_by_names": "forged"}, format="json")
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertNotIn("email", response.data)
        self.assertNotIn("password", response.data)

    def test_public_responses_only_expose_gallery_and_star_fields(self):
        self.item.starred_by.add(self.visitor)
        expected_fields = {
            "id", "title", "caption", "category", "location", "year", "image", "featured",
            "star_count", "is_starred", "starred_by_names",
        }
        for user in (None, self.visitor, self.editor, self.owner):
            self.client.force_authenticate(user)
            with self.subTest(user=user):
                listing = self.client.get(self.list_url)
                detail = self.client.get(self.detail_url)
                self.assertEqual(listing.status_code, 200)
                self.assertEqual(detail.status_code, 200)
                for data in (listing.data[0], detail.data):
                    self.assertEqual(set(data), expected_fields)
                    self.assertEqual(data["star_count"], 1)
                    self.assertEqual(data["is_starred"], user == self.visitor)
                    self.assertNotIn(self.visitor.email, str(data))
                    self.assertNotIn(self.visitor.password, str(data))

    def test_create_ignores_injected_star_fields(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "id": 123456, "star_count": 50, "is_starred": True,
            "starred_by_names": "fake", "starred_by": [self.visitor.pk],
        }, format="json")
        self.assertEqual(response.status_code, 201)
        item = GalleryItem.objects.get(pk=response.data["id"])
        self.assertNotEqual(item.pk, 123456)
        self.assertEqual(item.starred_by.count(), 0)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_real_session_csrf_for_update_delete_and_star(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="editor", password="test-password"))
        before = list(GalleryItem.objects.values())
        self.assertEqual(client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
        self.assertEqual(client.post(self.star_url).status_code, 403)
        self.assertEqual(list(GalleryItem.objects.values()), before)
        self.assertEqual(self.item.starred_by.count(), 0)
        client.get(reverse("main:show_gallery"))
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.patch(self.detail_url, {"title": "Changed"}, format="json", HTTP_X_CSRFTOKEN=token).status_code, 200)
        self.assertEqual(client.post(self.star_url, HTTP_X_CSRFTOKEN=token).status_code, 200)
        client.logout()
        self.assertTrue(client.login(username="owner", password="test-password"))
        before = list(GalleryItem.objects.values())
        self.assertEqual(client.delete(self.detail_url).status_code, 403)
        self.assertEqual(list(GalleryItem.objects.values()), before)
        client.get(reverse("main:show_gallery"))
        self.assertEqual(client.delete(self.detail_url, HTTP_X_CSRFTOKEN=client.cookies["csrftoken"].value).status_code, 204)

    def test_real_session_create_requires_csrf(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        before = list(GalleryItem.objects.values())
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(list(GalleryItem.objects.values()), before)
        client.get(reverse("main:show_gallery"))
        response = client.post(self.list_url, self.payload, format="json",
                              HTTP_X_CSRFTOKEN=client.cookies["csrftoken"].value)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(GalleryItem.objects.filter(pk=response.data["id"]).exists())

    def test_browsable_api_and_missing_mutation_targets(self):
        self.assertEqual(self.client.get(self.list_url, HTTP_ACCEPT="text/html").status_code, 200)
        self.client.force_authenticate(self.owner)
        detail = reverse("api:gallery-detail", args=[99999])
        before = list(GalleryItem.objects.values())
        for method in ("put", "patch", "delete"):
            with self.subTest(method=method):
                response = getattr(self.client, method)(detail, self.payload, format="json")
                self.assertEqual(response.status_code, 404)
        self.assertEqual(self.client.post(reverse("api:gallery-star", args=[99999])).status_code, 404)
        self.assertEqual(list(GalleryItem.objects.values()), before)

    def test_legacy_gallery_views_keep_the_same_roles(self):
        for user in (self.visitor, self.editor):
            self.client.force_login(user)
            before = list(GalleryItem.objects.values())
            self.assertEqual(self.client.post(reverse("main:create_gallery_item"), self.payload).status_code, 403)
            self.assertEqual(self.client.post(reverse("main:delete_gallery_item", args=[self.item.pk])).status_code, 403)
            self.assertEqual(self.client.post(reverse("main:create_gallery_item_ajax"), self.payload).status_code, 403)
            self.assertEqual(list(GalleryItem.objects.values()), before)
        self.client.force_login(self.editor)
        response = self.client.post(reverse("main:update_gallery_item", args=[self.item.pk]),
                                    {**self.payload, "title": "Editor via form lama"})
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, "Editor via form lama")

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
