from uuid import UUID

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied

from ..services import GetProjectsService, CreateProjectService
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


class CreateProjectServiceTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')

	def test_create_with_admin_user(self):
		service = CreateProjectService(self.user)
		project = service.create(
			title='new project', description='some description',
			category=self.category
		)
		self.assertIsInstance(project.pk, UUID)
		self.assertEqual(project.title, 'new project')
		self.assertEqual(project.description, 'some description')
		self.assertEqual(project.category, self.category)
		self.assertEqual(project.user, self.user)

	def test_create_with_not_authenticated_user(self):
		with self.assertRaises(PermissionDenied):
			CreateProjectService(AnonymousUser())

	def test_create_with_simple_user(self):
		simple_user = User.objects.create_user(
			username='someuser', password='somepass'
		)
		with self.assertRaises(PermissionDenied):
			CreateProjectService(simple_user)
