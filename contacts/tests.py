from urllib.parse import urlencode

from django.test import Client, TestCase
from django.urls import reverse

from .models import Contact


class ContactTests(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(name="Ani", email="ani@example.com", phone="08123456789")

    def url(self, action, pk=None):
        return reverse(f"contacts:contact_{action}", args=[pk] if pk is not None else [])

    def test_list_and_model(self):
        response = self.client.get(self.url("list"))
        self.assertContains(response, "Ani")
        self.assertContains(response, self.contact.phone)
        self.assertContains(response, 'hx-swap="beforeend"')
        self.assertEqual(str(self.contact), "Ani")

    def test_empty_list(self):
        Contact.objects.all().delete()
        self.assertContains(self.client.get(self.url("list")), "Tidak ada kontak.")

    def test_create_returns_only_new_row_and_oob_feedback(self):
        response = self.client.post(self.url("add"), {
            "name": "Budi", "email": "budi@example.com", "phone": "+62 812 3456",
        })
        contact = Contact.objects.get(name="Budi")
        self.assertContains(response, f'id="contact-{contact.pk}"')
        self.assertContains(response, 'hx-swap-oob="true"')
        self.assertContains(response, "Kontak berhasil ditambahkan!")
        self.assertNotContains(response, self.contact.email)
        self.assertNotContains(response, "<html")

    def test_phone_is_optional(self):
        response = self.client.post(self.url("add"), {"name": "Budi", "email": "budi@example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.get(name="Budi").phone, "")

    def test_invalid_create_does_not_save(self):
        for data in [
            {}, {"name": "   ", "email": "valid@example.com"},
            {"name": "Budi", "email": "invalid"},
            {"name": "x" * 101, "email": "valid@example.com"},
            {"name": "Budi", "email": "valid@example.com", "phone": "1" * 31},
        ]:
            with self.subTest(data=data):
                response = self.client.post(self.url("add"), data)
                self.assertEqual(response.status_code, 422)
                self.assertContains(response, 'id="feedback"', status_code=422)
                self.assertEqual(Contact.objects.count(), 1)

    def test_live_search_case_insensitive_and_empty_query(self):
        Contact.objects.create(name="Budi", email="budi@example.com")
        response = self.client.get(self.url("search"), {"q": " AN "})
        self.assertContains(response, "ani@example.com")
        self.assertNotContains(response, "budi@example.com")
        self.assertNotContains(response, "<html")
        self.assertContains(self.client.get(self.url("search")), "budi@example.com")
        self.assertContains(self.client.get(self.url("search"), {"q": "xyz"}), "Tidak ada kontak.")

    def test_edit_and_cancel_do_not_change_database(self):
        response = self.client.get(self.url("edit", self.contact.pk))
        self.assertContains(response, f'form="edit-form-{self.contact.pk}"')
        self.assertContains(response, self.contact.phone)
        self.assertContains(self.client.get(self.url("row", self.contact.pk)), "Ani")
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, "Ani")

    def test_put_updates_all_fields_including_unicode(self):
        response = self.client.put(self.url("update", self.contact.pk),
            urlencode({"name": "Dewi & José", "email": "dewi@example.com", "phone": "+62 811"}),
            content_type="application/x-www-form-urlencoded")
        self.assertContains(response, "Dewi &amp; José")
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, "Dewi & José")
        self.assertEqual(self.contact.phone, "+62 811")
        self.assertEqual(self.contact.email, "dewi@example.com")

    def test_invalid_update_preserves_database_and_form_values(self):
        response = self.client.put(self.url("update", self.contact.pk),
            urlencode({"name": "Budi", "email": "invalid", "phone": "123"}),
            content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 422)
        self.assertContains(response, 'value="invalid"', status_code=422)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, "Ani")
        self.assertEqual(self.contact.email, "ani@example.com")

    def test_delete_returns_empty_200(self):
        response = self.client.delete(self.url("delete", self.contact.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"")
        self.assertFalse(Contact.objects.exists())

    def test_missing_contact_returns_404(self):
        for action, method in [("edit", "get"), ("row", "get"), ("update", "put"), ("delete", "delete")]:
            with self.subTest(action=action):
                self.assertEqual(getattr(self.client, method)(self.url(action, 99999)).status_code, 404)

    def test_methods_are_restricted(self):
        for action in ["add", "update", "delete"]:
            pk = None if action == "add" else self.contact.pk
            self.assertEqual(self.client.get(self.url(action, pk)).status_code, 405)
        for action in ["list", "search", "edit", "row"]:
            pk = self.contact.pk if action in ["edit", "row"] else None
            self.assertEqual(self.client.post(self.url(action, pk)).status_code, 405)

    def test_csrf_required_for_all_mutations(self):
        client = Client(enforce_csrf_checks=True)
        data = {"name": "Budi", "email": "budi@example.com", "phone": "123"}
        for action, method in [("add", "post"), ("update", "put"), ("delete", "delete")]:
            pk = None if action == "add" else self.contact.pk
            self.assertEqual(getattr(client, method)(self.url(action, pk)).status_code, 403)
        client.get(self.url("list"))
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.post(self.url("add"), data, HTTP_X_CSRFTOKEN=token).status_code, 200)
        self.assertEqual(client.put(self.url("update", self.contact.pk), urlencode(data),
            content_type="application/x-www-form-urlencoded", HTTP_X_CSRFTOKEN=token).status_code, 200)
        self.assertEqual(client.delete(self.url("delete", self.contact.pk), HTTP_X_CSRFTOKEN=token).status_code, 200)

    def test_html_is_escaped_in_rows_and_forms(self):
        self.contact.name = '<script>alert("x")</script>'
        self.contact.save()
        for action in ["row", "edit"]:
            response = self.client.get(self.url(action, self.contact.pk))
            self.assertNotContains(response, '<script>alert("x")</script>')
            self.assertContains(response, "&lt;script&gt;")
