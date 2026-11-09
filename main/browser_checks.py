"""Optional integration checks: python manage.py test main.browser_checks."""
import os
import json
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client

from .models import GalleryItem, Project


class PortfolioBrowserChecks(StaticLiveServerTestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser("owner", "owner@example.com", "test-password")
        self.project = Project.objects.create(title="Portfolio", description="My website", tech_stack="Django")
        GalleryItem.objects.all().delete()
        self.gallery = GalleryItem.objects.create(title="Seed Gallery", year=2026, image="/static/img/kawah-ratu.jpeg")
        self.editor = User.objects.create_user("editor", password="test-password")
        self.editor.groups.add(Group.objects.get_or_create(name="Editor")[0])
        self.visitor = User.objects.create_user("visitor", password="test-password")
        editor_client = Client()
        editor_client.force_login(self.editor)
        self.editor_session = editor_client.cookies[settings.SESSION_COOKIE_NAME].value
        visitor_client = Client()
        visitor_client.force_login(self.visitor)
        self.visitor_session = visitor_client.cookies[settings.SESSION_COOKIE_NAME].value
        self.client.force_login(self.owner)
        session = self.client.cookies[settings.SESSION_COOKIE_NAME].value
        from playwright.sync_api import sync_playwright
        self.playwright = sync_playwright().start()
        self.addCleanup(self.playwright.stop)
        self.browser = self.playwright.chromium.launch(channel=os.getenv("CONTACTS_BROWSER_CHANNEL") or None)
        self.addCleanup(self.browser.close)
        self.context = self.browser.new_context()
        self.context.add_cookies([{"name": settings.SESSION_COOKIE_NAME, "value": session,
                                  "url": self.live_server_url}])
        self.page = self.context.new_page()
        self.errors = []
        self.page.on("pageerror", lambda error: self.errors.append(str(error)))

    def test_projects_ajax_create_patch_star_delete_and_errors(self):
        from playwright.sync_api import expect
        page = self.page
        with page.expect_response(lambda r: '/api/v1/projects/' in r.url and r.request.method == 'GET') as response:
            page.goto(self.live_server_url + '/projects/')
        self.assertEqual(response.value.status, 200)
        expect(page.locator('#grid article')).to_have_count(1)
        page.evaluate("window.pageMarker = 'same-document'")
        page.locator('[popovertarget="add-project-modal"]').first.click()
        form = page.locator('#project-form')
        form.locator('[name="title"]').fill('New browser project')
        form.locator('[name="description"]').fill('A useful app')
        form.locator('[name="tech_stack"]').fill('Python')
        with page.expect_response(lambda r: '/api/v1/projects/' in r.url and r.request.method == 'POST') as response:
            form.locator('[type="submit"]').click()
        self.assertEqual(response.value.status, 201)
        expect(page.locator('#grid article')).to_have_count(2)
        page.locator('#search-input').fill('New browser')
        expect(page.locator('#grid article')).to_have_count(1)
        page.locator('[data-action="star"]').click()
        expect(page.locator('[data-action="star"]')).to_contain_text('Unstar (1)')
        page.locator('[data-action="star"]').click()
        expect(page.locator('[data-action="star"]')).to_contain_text('Star (0)')
        page.once('dialog', lambda dialog: dialog.accept())
        with page.expect_response(lambda r: r.request.method == 'DELETE') as response:
            page.locator('[data-action="delete"]').click()
        self.assertEqual(response.value.status, 204)
        expect(page.locator('#empty')).to_be_visible()
        page.locator('#search-input').fill('Portfolio')
        expect(page.locator('#grid article')).to_have_count(1)
        result = page.evaluate("""async id => {
            await writeProject(projectEndpoint(DETAIL_PROJECT_ENDPOINT, id), 'PATCH', {title: 'Updated project'});
            return true;
        }""", str(self.project.pk))
        self.assertTrue(result)
        page.locator('#search-input').fill('Updated')
        expect(page.locator('#grid article h2')).to_have_text('Updated project')
        page.route('**/api/v1/projects/?*', lambda route: route.abort())
        page.locator('#search-input').fill('offline')
        expect(page.locator('#error')).to_be_visible()
        self.assertEqual(page.evaluate('window.pageMarker'), 'same-document')
        self.assertEqual(self.errors, [])

    def test_guest_ui_and_logged_in_star_without_old_csrf_cookie(self):
        from playwright.sync_api import expect
        page = self.page
        page.goto(self.live_server_url + '/projects/')
        expect(page.locator('[data-action="star"]')).to_have_count(1)
        self.assertTrue(any(c['name'] == 'csrftoken' for c in self.context.cookies()))
        page.locator('[data-action="star"]').click()
        expect(page.locator('[data-action="star"]')).to_contain_text('Unstar')
        self.context.clear_cookies()
        page.reload()
        expect(page.locator('#grid article')).to_have_count(1)
        expect(page.get_by_role('link', name='Login untuk star (1)')).to_be_visible()
        expect(page.locator('[data-action="delete"]')).to_have_count(0)
        expect(page.locator('#project-form')).to_have_count(0)
        self.assertEqual(self.errors, [])

    def test_gallery_owner_create_star_edit_delete(self):
        from playwright.sync_api import expect
        page = self.page
        page.goto(self.live_server_url + '/gallery/')
        expect(page.locator('#gallery-grid article')).to_have_count(1)
        page.evaluate("window.galleryMarker = 'same-document'")
        page.locator('[popovertarget="add-gallery-modal"]').first.click()
        form = page.locator('#gallery-form')
        for name, value in {'title': 'Browser gallery', 'caption': 'A moment', 'category': 'Travel',
                            'location': 'Bogor', 'year': '2026', 'image': self.live_server_url + '/static/img/kawah-ratu.jpeg'}.items():
            form.locator(f'[name="{name}"]').fill(value)
        form.locator('[name="featured"]').check()
        with page.expect_response(lambda r: '/api/v1/gallery/' in r.url and r.request.method == 'POST') as response:
            form.locator('[type="submit"]').click()
        self.assertEqual(response.value.status, 201)
        self.assertTrue(response.value.json()['featured'])
        expect(page.locator('#gallery-grid article')).to_have_count(2)
        page.locator('#gallery-search-input').fill('Browser gallery')
        expect(page.locator('#gallery-grid article')).to_have_count(1)
        page.locator('[data-action="star"]').click()
        expect(page.locator('[data-action="star"]')).to_contain_text('Unstar (1)')
        page.locator('[data-action="edit"]').click()
        edit_form = page.locator('#gallery-edit-form')
        expect(edit_form.locator('[name="title"]')).to_have_value('Browser gallery')
        expect(edit_form.locator('[name="featured"]')).to_be_checked()
        edit_form.locator('[name="title"]').fill('Browser gallery updated')
        edit_form.locator('[name="featured"]').uncheck()
        with page.expect_response(lambda r: r.request.method == 'PATCH') as response:
            edit_form.get_by_role('button', name='Simpan Perubahan').click()
        self.assertEqual(response.value.status, 200)
        self.assertFalse(response.value.json()['featured'])
        expect(page.locator('#gallery-grid article')).to_have_count(1)
        expect(page.locator('#gallery-grid h2')).to_have_text('Browser gallery updated')
        expect(page.locator('#gallery-search-input')).to_have_value('Browser gallery')
        self.assertEqual(page.evaluate('window.galleryMarker'), 'same-document')
        page.once('dialog', lambda dialog: dialog.accept())
        with page.expect_response(lambda r: r.request.method == 'DELETE') as response:
            page.locator('[data-action="delete"]').click()
        self.assertEqual(response.value.status, 204)
        expect(page.locator('#gallery-empty')).to_be_visible()
        self.assertEqual(self.errors, [])

    def test_gallery_editor_can_update_but_has_no_create_delete_buttons(self):
        from playwright.sync_api import expect
        self.context.clear_cookies()
        self.context.add_cookies([{'name': settings.SESSION_COOKIE_NAME, 'value': self.editor_session, 'url': self.live_server_url}])
        page = self.page
        page.goto(self.live_server_url + '/gallery/')
        expect(page.locator('#gallery-grid article')).to_have_count(1)
        expect(page.locator('[data-action="delete"]')).to_have_count(0)
        expect(page.locator('#gallery-form')).to_have_count(0)
        page.locator('[data-action="edit"]').click()
        page.locator('#gallery-edit-form [name="title"]').fill('Editor update')
        with page.expect_response(lambda r: r.request.method == 'PATCH') as response:
            page.get_by_role('button', name='Simpan Perubahan').click()
        self.assertEqual(response.value.status, 200)
        expect(page.locator('#gallery-grid h2')).to_have_text('Editor update')
        page.set_viewport_size({'width': 390, 'height': 844})
        page.locator('[data-action="edit"]').click()
        expect(page.locator('#edit-gallery-modal')).to_be_visible()
        bounds = page.locator('#edit-gallery-modal .project-form-modal__content').bounding_box()
        self.assertGreaterEqual(bounds['x'], 0)
        self.assertLessEqual(bounds['x'] + bounds['width'], 390)
        screenshot_dir = os.getenv('PORTFOLIO_SCREENSHOT_DIR')
        if screenshot_dir:
            Path(screenshot_dir).mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(Path(screenshot_dir) / 'gallery-edit-mobile.png'))
        self.assertEqual(self.errors, [])

    def test_gallery_validation_errors_xss_and_retry(self):
        from playwright.sync_api import expect
        page = self.page
        page.goto(self.live_server_url + '/gallery/')
        expect(page.locator('#gallery-grid article')).to_have_count(1)
        dialogs = []
        page.on('dialog', lambda dialog: (dialogs.append(dialog.message), dialog.dismiss()))
        page.locator('[popovertarget="add-gallery-modal"]').first.click()
        form = page.locator('#gallery-form')
        form.locator('[name="title"]').fill('<img src="x" onerror="alert(1)">')
        form.locator('[name="year"]').fill('2026')
        form.locator('[name="image"]').fill('/static/img/kawah-ratu.jpeg')
        with page.expect_response(lambda r: r.request.method == 'POST') as response:
            form.locator('[type="submit"]').click()
        self.assertEqual(response.value.status, 400)
        expect(page.locator('#toast-component')).to_contain_text('Judul foto')
        expect(page.locator('#add-gallery-modal')).to_be_visible()
        expect(form.locator('[name="title"]')).to_have_value('<img src="x" onerror="alert(1)">')
        self.assertEqual(len(page.request.get(self.live_server_url + '/api/v1/gallery/').json()), 1)
        form.get_by_role('button', name='Batal').click()

        page.locator('[data-action="edit"]').click()
        edit_form = page.locator('#gallery-edit-form')
        edit_form.locator('[name="title"]').fill('Belum disimpan')
        page.route('**/api/v1/gallery/*/', lambda route: route.fulfill(
            status=403, content_type='application/json', body='{"detail":"Akses edit ditolak."}'
        ) if route.request.method == 'PATCH' else route.continue_())
        edit_form.get_by_role('button', name='Simpan Perubahan').click()
        expect(page.locator('#toast-component')).to_contain_text('Akses edit ditolak.')
        expect(edit_form.locator('[name="title"]')).to_have_value('Belum disimpan')
        saved_item = page.request.get(self.live_server_url + f'/api/v1/gallery/{self.gallery.pk}/').json()
        self.assertEqual(saved_item['title'], 'Seed Gallery')
        edit_form.get_by_role('button', name='Batal').click()
        page.unroute('**/api/v1/gallery/*/')

        result = page.evaluate("""() => {
            const card = buildGalleryCardElement({id: 1, title: '<img src=x onerror=alert(1)>',
                caption: '<script>alert(1)</scr' + 'ipt>', category: '<b>Travel</b>',
                location: '\" onmouseover=\"alert(1)', year: 2026, image: 'javascript:alert(1)',
                star_count: 0, is_starred: false, starred_by_names: '\" onclick=\"alert(1)'});
            return {images: card.querySelectorAll('img').length, scripts: card.querySelectorAll('script').length,
                events: card.querySelectorAll('[onerror], [onclick], [onmouseover]').length, text: card.textContent};
        }""")
        self.assertEqual(result['images'], 0)
        self.assertEqual(result['scripts'], 0)
        self.assertEqual(result['events'], 0)
        self.assertIn('<img src=x onerror=alert(1)>', result['text'])
        self.assertEqual(dialogs, [])

        page.route('**/api/v1/gallery/?*', lambda route: route.abort())
        page.locator('#gallery-search-input').fill('offline')
        expect(page.locator('#gallery-error')).to_be_visible()
        page.unroute('**/api/v1/gallery/?*')
        page.locator('#gallery-search-input').fill('Seed')
        page.locator('#gallery-retry').click()
        expect(page.locator('#gallery-grid article')).to_have_count(1)
        self.assertEqual(self.errors, [])

    def test_gallery_guest_and_visitor_on_desktop_and_mobile(self):
        from playwright.sync_api import expect
        page = self.page
        self.context.clear_cookies()
        for width, height in ((1365, 900), (390, 844)):
            page.set_viewport_size({'width': width, 'height': height})
            page.goto(self.live_server_url + '/gallery/')
            expect(page.locator('#gallery-grid article')).to_have_count(1)
            expect(page.get_by_role('link', name='Login untuk star (0)')).to_be_visible()
            expect(page.locator('#gallery-form')).to_have_count(0)
            expect(page.locator('#gallery-edit-form')).to_have_count(0)
            self.assertTrue(page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'))
            screenshot_dir = os.getenv('PORTFOLIO_SCREENSHOT_DIR')
            if screenshot_dir:
                Path(screenshot_dir).mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(Path(screenshot_dir) / f'gallery-{width}.png'), full_page=True)
        self.context.add_cookies([{'name': settings.SESSION_COOKIE_NAME,
            'value': self.visitor_session, 'url': self.live_server_url}])
        page.goto(self.live_server_url + '/gallery/')
        expect(page.locator('[data-action="star"]')).to_have_count(1)
        expect(page.locator('[data-action="edit"]')).to_have_count(0)
        expect(page.locator('[data-action="delete"]')).to_have_count(0)
        self.assertTrue(any(c['name'] == 'csrftoken' for c in self.context.cookies()))
        page.locator('[data-action="star"]').click()
        expect(page.locator('[data-action="star"]')).to_contain_text('Unstar (1)')
        self.assertEqual(self.errors, [])

    def test_gallery_loading_debounce_and_empty_results(self):
        from playwright.sync_api import expect
        page = self.page
        pending = []
        page.route('**/api/v1/gallery/', lambda route: pending.append(route))
        page.goto(self.live_server_url + '/gallery/')
        expect(page.locator('#gallery-loading')).to_be_visible()
        self.assertEqual(len(pending), 1)
        pending[0].fulfill(status=200, content_type='application/json', body=json.dumps([{
            'id': self.gallery.pk, 'title': 'Seed Gallery', 'caption': '', 'category': '',
            'location': '', 'year': 2026, 'image': '/static/img/kawah-ratu.jpeg',
            'featured': False, 'star_count': 0, 'is_starred': False, 'starred_by_names': '',
        }]))
        expect(page.locator('#gallery-grid article')).to_have_count(1)
        page.unroute('**/api/v1/gallery/')
        queries = []
        page.on('request', lambda request: queries.append(request.url)
                if '/api/v1/gallery/?title=' in request.url else None)
        search = page.locator('#gallery-search-input')
        search.fill('S')
        search.fill('Se')
        with page.expect_response(lambda r: '/api/v1/gallery/?title=Seed' in r.url) as response:
            search.fill('Seed')
        self.assertEqual(response.value.status, 200)
        self.assertEqual(len(queries), 1)
        search.fill('Tidak ditemukan')
        expect(page.locator('#gallery-empty')).to_be_visible()
        expect(page.locator('#gallery-grid')).to_be_hidden()
        self.assertEqual(self.errors, [])

    def test_xss_escaping_and_validation_feedback(self):
        from playwright.sync_api import expect
        page = self.page
        page.goto(self.live_server_url + '/projects/')
        expect(page.locator('#grid article')).to_have_count(1)
        result = page.evaluate("""() => {
            const card = buildProjectCardElement({id: '00000000-0000-0000-0000-000000000000',
                title: '<img src=x onerror=alert(1)>', description: '<script>alert(1)</scr' + 'ipt>',
                tech_stack: '<b>Django</b>', project_url: 'javascript:alert(1)',
                project_image_url: 'javascript:alert(1)', star_count: 0, starred_by_names: '" onmouseover="alert(1)'});
            return {html: card.innerHTML, images: card.querySelectorAll('img').length,
                scripts: card.querySelectorAll('script').length, text: card.textContent};
        }""")
        self.assertEqual(result['images'], 0)
        self.assertEqual(result['scripts'], 0)
        self.assertIn('<img src=x onerror=alert(1)>', result['text'])
        page.locator('[popovertarget="add-project-modal"]').first.click()
        form = page.locator('#project-form')
        form.locator('[name="title"]').fill('   ')
        form.locator('[name="description"]').fill('Description')
        form.locator('[name="tech_stack"]').fill('Django')
        with page.expect_response(lambda r: r.request.method == 'POST' and '/api/v1/projects/' in r.url) as response:
            form.locator('[type="submit"]').click()
        self.assertEqual(response.value.status, 400)
        expect(page.locator('#toast-component')).to_contain_text('Belum berhasil')
        expect(form.locator('[name="title"]')).to_have_value('   ')
        self.assertEqual(self.errors, [])
