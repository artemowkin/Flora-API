from django.test import TestCase
from django.contrib.auth import get_user_model

from categories.models import Category


User = get_user_model()


class AllCreateCategoriesEndpointTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
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

	def test_create_with_not_authenticated_user(self):
		response = self._request_create_category()
		self.assertEqual(response.status_code, 403)

	def _request_create_category(self):
		return self.client.post('/api/v1/categories/', {
			'title': 'new category'
		}, content_type='application/json')

	def test_create_with_simple_user(self):
		simple_user = User.objects.create_user(
			username='simpleuser', password='simplepass'
		)
		self.client.login(username='simpleuser', password='simplepass')
		response = self._request_create_category()
		self.assertEqual(response.status_code, 403)

	def test_create(self):
		self.client.login(username='testuser', password='testpass')
		response = self._request_create_category()
		self.assertEqual(response.status_code, 201)
		json_response = response.json()
		self.assertIn('pk', json_response)
		self.assertEqual(json_response['title'], 'new category')
