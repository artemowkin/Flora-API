from django.test import TestCase
from django.urls import reverse


class AllCreateCategoriesViewTestCase(TestCase):

	def test_get(self):
		response = self.client.get(reverse('all_create_categories'))
		self.assertEqual(response.status_code, 200)
