from django.core.urlresolvers import reverse
from django.test import TestCase

class AboutViewTest(TestCase):
    fixtures = ['sites', 'stores']

    def setUp(self):
        from jobim.models import Store

        self.store = Store.objects.get(pk=1)
        self.url_kwargs = {'kwargs': {'store_url': self.store.url}}

    def test_about(self):
        response = self.client.get(reverse('jobim:about', **self.url_kwargs))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'jobim/about.html')
        self.assertContains(response, 'Ele serve para sabermos quanto as pess')
