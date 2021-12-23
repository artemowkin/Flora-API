from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from projects.models import Project
from categories.models import Category


User = get_user_model()


class LikeProjectViewTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='test category')
		self.project = Project.objects.create(
			title='test project', description='test description',
			category=self.category, user=self.user
		)

	def test_post(self):
		self.client.login(username='testuser', password='testpass')
		request = self.client.post(
			reverse('like_project', args=[self.project.pk])
		)
		self.assertEqual(request.status_code, 200)
