from django.test import TestCase
from django.urls import reverse


class AllCreateProjectsViewTestCase(TestCase):

	def test_get(self):
		response = self.client.get(reverse('all_create_projects'))
		self.assertEqual(response.status_code, 200)
