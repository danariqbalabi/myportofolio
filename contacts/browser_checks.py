"""Optional browser integration tests: python manage.py test contacts.browser_checks."""
import os
from pathlib import Path
from tempfile import gettempdir

from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class ContactBrowserChecks(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        from playwright.sync_api import sync_playwright

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(channel=os.getenv("CONTACTS_BROWSER_CHANNEL") or None)

    def tearDown(self):
        self.browser.close()
        self.playwright.stop()
        super().tearDown()

    def test_htmx_crud_validation_search_and_empty_state(self):
        from playwright.sync_api import expect

        page = self.browser.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(self.live_server_url + "/contacts/")
        page.evaluate("window.pageMarker = 'same-document'")
        expect(page.locator(".empty-row")).to_be_visible()

        def add(name, email):
            page.locator("#id_name").fill(name)
            page.locator("#id_email").fill(email)
            page.locator("#id_phone").fill("08123456789")
            page.get_by_role("button", name="Tambah", exact=True).click()
            expect(page.locator("#feedback")).to_have_text("Kontak berhasil ditambahkan!")
            expect(page.locator("#id_name")).to_have_value("")

        add("Ani", "ani@example.com")
        expect(page.locator(".contact-row")).to_have_count(1)
        expect(page.locator(".empty-row")).to_be_hidden()
        add("Budi", "budi@example.com")
        expect(page.locator(".contact-row")).to_have_count(2)

        # Trigger server validation, bypassing native browser validation.
        page.locator("#add-contact-form").evaluate("form => form.noValidate = true")
        page.locator("#id_name").fill("Invalid")
        page.locator("#id_email").fill("invalid")
        page.get_by_role("button", name="Tambah", exact=True).click()
        expect(page.locator("#feedback")).to_contain_text("Kontak belum disimpan")
        expect(page.locator("#id_name")).to_have_value("Invalid")
        expect(page.locator(".contact-row")).to_have_count(2)

        search = page.locator("#contact-search")
        search.fill("ANI")
        expect(page.locator(".contact-row")).to_have_count(1)
        expect(page.locator(".contact-row")).to_contain_text("Ani")
        search.fill("missing")
        expect(page.locator(".contact-row")).to_have_count(0)
        expect(page.locator(".empty-row")).to_be_visible()
        search.fill("")
        expect(page.locator(".contact-row")).to_have_count(2)

        row = page.locator(".contact-row").first
        row.get_by_role("button", name="Edit", exact=True).click()
        expect(row.locator('[name="name"]')).to_be_visible()
        row.locator('[name="name"]').fill("Dewi")
        row.get_by_role("button", name="Batal", exact=True).click()
        expect(row).to_contain_text("Ani")
        row.get_by_role("button", name="Edit", exact=True).click()
        row.locator("form").evaluate("form => form.noValidate = true")
        row.locator('[name="email"]').fill("invalid")
        row.get_by_role("button", name="Simpan", exact=True).click()
        expect(row.locator(".errorlist")).to_be_visible()
        expect(row.locator('[name="email"]')).to_have_value("invalid")
        row.locator('[name="name"]').fill("Dewi & José")
        row.locator('[name="email"]').fill("dewi@example.com")
        row.locator('[name="phone"]').fill("+62 811")
        row.get_by_role("button", name="Simpan", exact=True).click()
        expect(row).to_contain_text("Dewi & José")
        expect(row).to_contain_text("+62 811")

        # Adding under an active filter restores the full list without duplicates.
        search.fill("Dewi")
        expect(page.locator(".contact-row")).to_have_count(1)
        add("Cici", "cici@example.com")
        expect(search).to_have_value("")
        expect(page.locator(".contact-row")).to_have_count(3)
        page.screenshot(path=str(Path(gettempdir()) / "tutorial6-desktop.png"), full_page=True)

        page.once("dialog", lambda dialog: dialog.dismiss())
        page.get_by_role("button", name="Hapus", exact=True).first.click()
        expect(page.locator(".contact-row")).to_have_count(3)
        page.on("dialog", lambda dialog: dialog.accept())
        for remaining in [2, 1, 0]:
            page.get_by_role("button", name="Hapus", exact=True).first.click()
            expect(page.locator(".contact-row")).to_have_count(remaining)
        expect(page.locator(".empty-row")).to_be_visible()
        self.assertEqual(page.evaluate("window.pageMarker"), "same-document")
        self.assertEqual(errors, [])
        page.close()

    def test_mobile_layout(self):
        page = self.browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(self.live_server_url + "/contacts/")
        self.assertTrue(page.evaluate("document.documentElement.scrollWidth <= innerWidth"))
        page.screenshot(path=str(Path(gettempdir()) / "tutorial6-mobile.png"), full_page=True)
        page.close()
