from django.test import TestCase
from django.contrib.auth import get_user_model

from ..services import GetProjectsService
from ..models import Project
from categories.models import Category


User = get_user_model()


class GetProjectsServiceTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')
		self.project = Project.objects.create(
			title='some project', description='some description',
			category=self.category, user=self.user
		)

	def test_get_all(self):
		service = GetProjectsService()
		all_projects = service.get_all()
		self.assertEqual(all_projects.count(), 1)
		self.assertEqual(all_projects[0], self.project)
