from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from categories.models import Category
from ..models import Project


User = get_user_model()


class AllCreateProjectsViewTestCase(TestCase):

	def test_get(self):
		response = self.client.get(reverse('all_create_projects'))
		self.assertEqual(response.status_code, 200)

	def test_post(self):
		user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		category = Category.objects.create(title='some category')
		self.client.login(username='testuser', password='testpass')
		response = self.client.post(
			reverse('all_create_projects'), {
				'title': 'some project', 'description': 'some description',
				'category': category.pk
			}, content_type="application/json"
		)
		self.assertEqual(response.status_code, 201)


class ConcreteProjectViewTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')
		self.project = Project.objects.create(
			title='some project', description='some description',
			category=self.category, user=self.user
		)

	def test_get(self):
		response = self.client.get(reverse(
			'concrete_project', args=[str(self.project.pk)]
		))
		self.assertEqual(response.status_code, 200)

	def test_put(self):
		self.client.login(username='testuser', password='testpass')
		response = self.client.put(
			reverse('concrete_project', args=[str(self.project.pk)]), {
				'title': 'new title', 'description': 'new description',
				'category': self.category.pk
			}, content_type="application/json"
		)
		self.assertEqual(response.status_code, 200)
