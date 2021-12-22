from django.test import TestCase

from categories.models import Category


class AllCreateCategoriesEndpointTestCase(TestCase):

	def setUp(self):
		self.category = Category.objects.create(title='some category')

	def test_get_all_categories(self):
		response = self.client.get('/api/v1/categories/')
		self.assertEqual(response.status_code, 200)
		json_response = response.json()
		self.assertEqual(len(json_response), 1)
		self.assertEqual(json_response[0], {
			'pk': str(self.category.pk),
			'title': 'some category'
		})
