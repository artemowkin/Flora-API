from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Category


User = get_user_model()


class AllCreateCategoriesViewTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)

	def test_get(self):
		response = self.client.get(reverse('all_create_categories'))
		self.assertEqual(response.status_code, 200)

	def test_post(self):
		self.client.login(username='testuser', password='testpass')
		response = self.client.post(reverse('all_create_categories'), {
			'title': 'new category'
		}, content_type='application/json')
		self.assertEqual(response.status_code, 201)


class ConcreteCategoryViewTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')

	def test_get(self):
		response = self.client.get(
			reverse('concrete_category', args=[self.category.pk])
		)
		self.assertEqual(response.status_code, 200)

	def test_put(self):
		self.client.login(username='testuser', password='testpass')
		response = self.client.put(
			reverse('concrete_category', args=[self.category.pk]), {
				'title': 'new category'
			}, content_type='application/json'
		)
		self.assertEqual(response.status_code, 200)
