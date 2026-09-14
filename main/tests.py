from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, GalleryItem, Highlight


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")


class ExperiencePageTest(TestCase):
    def setUp(self):
        self.experiences = [
            Experience.objects.create(
                title="VPIC Of Public Relations",
                description="Vice Person in Charge of Public Relations Division.",
                category="full-time",
                thumbnail="/static/img/openhouse.png",
            ),
            Experience.objects.create(
                title="Member of Product & Project Management",
                description="Member of Product and Project Management RISTEK Fasilkom UI.",
                category="full-time",
                thumbnail="/static/img/ristek.png",
            ),
            Experience.objects.create(
                title="Awardee of Beasiswa Unggulan",
                description="Awardee of Beasiswa Unggulan from Kemendikbud.",
                category="full-time",
                thumbnail="/static/img/bu.png",
            ),
        ]

    def test_experience_url_and_template(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")

    def test_experience_data_and_images_are_saved(self):
        response = self.client.get(reverse("main:show_experience"))

        for experience in self.experiences:
            self.assertContains(response, experience.title, html=True)
            self.assertContains(response, experience.description)
            self.assertContains(response, experience.thumbnail)

    def test_empty_experience_message(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")


class HighlightsPageTest(TestCase):
    def setUp(self):
        self.highlights = [
            Highlight.objects.create(
                title="5-Day Exchange Program University of Malaya",
                description="Academic exchange program at the University of Malaya.",
                category="Academic Exchange",
                year=2026,
                thumbnail="/static/img/exchange-um.png",
            ),
            Highlight.objects.create(
                title="Semifinalist BPC UISP 2025",
                description="Product: Bring.In",
                category="Business Case Competition",
                year=2025,
                thumbnail="/static/img/bpc-uisp.jpg",
            ),
            Highlight.objects.create(
                title="3rd Winner Pekan RISTEK 2025",
                description="Third winner of the Pekan RISTEK mini case competition.",
                category="Mini Case Competition",
                year=2025,
                thumbnail="/static/img/pekan-ristek.jpg",
            ),
            Highlight.objects.create(
                title="Semifinalist BPC EPIC 11th",
                description="Product: Bring.In",
                category="Business Case Competition",
                year=2025,
                thumbnail="/static/img/bpc-epic.jpg",
            ),
        ]

    def test_highlights_url_and_template(self):
        response = self.client.get(reverse("main:show_highlights"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "highlights.html")

    def test_highlight_data_and_images_are_displayed(self):
        response = self.client.get(reverse("main:show_highlights"))

        for highlight in self.highlights:
            self.assertContains(response, highlight.title)
            self.assertContains(response, highlight.description)
            self.assertContains(response, highlight.thumbnail)

    def test_empty_highlights_message(self):
        Highlight.objects.all().delete()
        response = self.client.get(reverse("main:show_highlights"))

        self.assertContains(response, "Belum ada highlight yang ditambahkan.")


class GalleryPageTest(TestCase):
    def setUp(self):
        self.gallery_items = [
            GalleryItem.objects.create(
                title="Kawah Ratu",
                caption="A hike through the Kawah Ratu trail.",
                category="Adventure",
                location="Gunung Salak, Jawa Barat",
                year=2025,
                image="/static/img/kawah-ratu.jpeg",
                featured=True,
            ),
            GalleryItem.objects.create(
                title="Gallery UM",
                caption="Academic exchange moments at the University of Malaya.",
                category="Academic Exchange",
                location="University of Malaya",
                year=2026,
                image="/static/img/gallery-um.jpeg",
            ),
            GalleryItem.objects.create(
                title="Raja Padel",
                caption="Alias saya jago banget main padel.",
                category="Sports",
                location="Raja Padel",
                year=2026,
                image="/static/img/raja-padel.jpeg",
                featured=True,
            ),
            GalleryItem.objects.create(
                title="Bandung dan Cilembeu",
                caption="Perjalanan ke Bandung dan Cilembeu.",
                category="Travel",
                location="Bandung dan Cilembeu, Jawa Barat",
                year=2026,
                image="/static/img/cilembeu.jpeg",
            ),
            GalleryItem.objects.create(
                title="Bangkok Bersama Keluarga",
                caption="Liburan bersama keluarga di Bangkok.",
                category="Family Trip",
                location="Bangkok, Thailand",
                year=2026,
                image="/static/img/bangkok.jpeg",
            ),
        ]

    def test_gallery_url_and_template(self):
        response = self.client.get(reverse("main:show_gallery"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "gallery.html")

    def test_gallery_data_and_images_are_displayed(self):
        response = self.client.get(reverse("main:show_gallery"))

        for item in self.gallery_items:
            self.assertContains(response, item.title)
            self.assertContains(response, item.caption)
            self.assertContains(response, item.image)

    def test_empty_gallery_message(self):
        GalleryItem.objects.all().delete()
        response = self.client.get(reverse("main:show_gallery"))

        self.assertContains(response, "Belum ada foto di gallery.")
