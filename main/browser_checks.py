"""Optional integration checks: python manage.py test main.browser_checks."""
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from .models import Project


class PortfolioBrowserChecks(StaticLiveServerTestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser("owner", "owner@example.com", "test-password")
        self.project = Project.objects.create(title="Portfolio", description="My website", tech_stack="Django")
        self.client.force_login(self.owner)
        session = self.client.cookies[settings.SESSION_COOKIE_NAME].value
        from playwright.sync_api import sync_playwright
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(channel=os.getenv("CONTACTS_BROWSER_CHANNEL", "msedge"))
        self.context = self.browser.new_context()
        self.context.add_cookies([{"name": settings.SESSION_COOKIE_NAME, "value": session,
                                  "url": self.live_server_url}])
        self.page = self.context.new_page()
        self.errors = []
        self.page.on("pageerror", lambda error: self.errors.append(str(error)))

    def tearDown(self):
        self.browser.close()
        self.playwright.stop()
        super().tearDown()

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
