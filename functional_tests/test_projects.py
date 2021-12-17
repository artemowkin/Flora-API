from django.test import TestCase
from django.contrib.auth import get_user_model

from categories.models import Category
from projects.models import Project, Project


User = get_user_model()


class AllCreateProjectsEndpointTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')
		self.project = Project.objects.create(
			title='some project', description='some description',
			category=self.category, user=self.user
		)

	def test_get_all_projects(self):
		response = self.client.get('/api/v1/projects/')
		self.assertEqual(response.status_code, 200)
		json = response.json()
		self.assertEqual(json, [{
			'pk': str(self.project.pk),
			'title': self.project.title,
			'description': self.project.description,
			'images': [],
			'category': str(self.category.pk),
			'user': self.user.username,
			'pub_datetime': self.project.pub_datetime.isoformat()[:-6]+'Z'
		}])
