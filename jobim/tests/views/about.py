from django.core.urlresolvers import reverse

from jobim.tests.helpers import ViewTestCase


class AboutViewTest(ViewTestCase):

    def test_uses_right_template(self):
        response = self.client.get(reverse('jobim:about', **self.url_kwargs))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'jobim/about.html')
        self.assertContains(response, 'Ele serve para sabermos quanto as pess')
