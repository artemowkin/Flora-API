from uuid import UUID, uuid4

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http import Http404

from ..services import (
	GetProjectsService, CreateProjectService, UpdateProjectService
)
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

	def test_get_concrete(self):
		service = GetProjectsService()
		concrete_project = service.get_concrete(self.project.pk)
		self.assertEqual(concrete_project, self.project)

	def test_get_concrete_with_unexisting_pk(self):
		service = GetProjectsService()
		with self.assertRaises(Http404):
			service.get_concrete(uuid4())


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


class UpdateProjectServiceTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')
		self.project = Project.objects.create(
			title='some project', description='some description',
			category=self.category, user=self.user
		)

	def test_update(self):
		service = UpdateProjectService(self.user)
		new_category = Category.objects.create(title='new category')
		project = service.update(
			self.project, 'New title', 'New description', new_category
		)
		self.assertEqual(project.pk, self.project.pk)
		self.assertEqual(project.title, 'New title')
		self.assertEqual(project.description, 'New description')
		self.assertEqual(project.category, new_category)
		self.assertEqual(project.user, self.user)

	def test_update_with_not_authenticated_user(self):
		with self.assertRaises(PermissionDenied):
			UpdateProjectService(AnonymousUser())

	def test_update_with_simple_user(self):
		simple_user = User.objects.create_user(
			username='someuser', password='somepass'
		)
		with self.assertRaises(PermissionDenied):
			UpdateProjectService(simple_user)
