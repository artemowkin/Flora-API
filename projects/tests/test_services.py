from uuid import UUID, uuid4

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http import Http404

from ..services import (
	GetProjectsService, CreateProjectService, UpdateProjectService,
	DeleteProjectService, pin_project, unpin_project, SearchProjectsService,
	get_pinned_projects
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
		self.assertEqual(concrete_project.pk, self.project.pk)
		self.assertEqual(concrete_project.views, 1)

	def test_get_concrete_with_unexisting_pk(self):
		service = GetProjectsService()
		with self.assertRaises(Http404):
			service.get_concrete(uuid4())


class GetPinnedProjectsTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')
		self.project = Project.objects.create(
			title='some project', description='some description',
			category=self.category, user=self.user
		)

	def test_get_pinned(self):
		new_project = Project.objects.create(
			title='some project', description='some description',
			category=self.category, user=self.user, pinned=True
		)
		pinned_projects = get_pinned_projects()
		self.assertEqual(len(pinned_projects), 1)
		self.assertEqual(pinned_projects[0], new_project)

	def test_get_pinned_with_more_than_20_pinned_projects(self):
		for i in range(21):
			Project.objects.create(
				title=f'new project{i}', description='some description',
				category=self.category, user=self.user, pinned=True
			)

		pinned_projects = get_pinned_projects()
		self.assertEqual(len(pinned_projects), 20)


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
			self.project.pk, 'New title', 'New description', new_category
		)
		self.assertEqual(project.pk, self.project.pk)
		self.assertEqual(project.title, 'New title')
		self.assertEqual(project.description, 'New description')
		self.assertEqual(project.category, new_category)
		self.assertEqual(project.user, self.user)
		self.assertEqual(project.views, 0)

	def test_update_with_not_authenticated_user(self):
		with self.assertRaises(PermissionDenied):
			UpdateProjectService(AnonymousUser())

	def test_update_with_simple_user(self):
		simple_user = User.objects.create_user(
			username='someuser', password='somepass'
		)
		with self.assertRaises(PermissionDenied):
			UpdateProjectService(simple_user)


class DeleteProjectServiceTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')
		self.project = Project.objects.create(
			title='some project', description='some description',
			category=self.category, user=self.user
		)

	def test_delete(self):
		service = DeleteProjectService(self.user)
		service.delete(self.project.pk)
		self.assertEqual(Project.objects.count(), 0)

	def test_delete_with_not_authenticated_user(self):
		with self.assertRaises(PermissionDenied):
			DeleteProjectService(AnonymousUser())

	def test_delete_with_simple_user(self):
		simple_user = User.objects.create_user(
			username='someuser', password='someuser'
		)
		with self.assertRaises(PermissionDenied):
			DeleteProjectService(simple_user)


class PinProjectServiceTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')
		self.project = Project.objects.create(
			title='some project', description='some description',
			category=self.category, user=self.user
		)

	def test_pin_with_not_pinned_project(self):
		resp = pin_project(self.project.pk)
		project = Project.objects.get(pk=self.project.pk)
		self.assertTrue(project.pinned)
		self.assertEqual(resp, {'pinned': True})

	def test_pin_with_already_pinned_project(self):
		self.project.pinned = True
		self.project.save()
		resp = pin_project(self.project.pk)
		project = Project.objects.get(pk=self.project.pk)
		self.assertTrue(project.pinned)
		self.assertEqual(resp, {'pinned': False})


class UnpinProjectServiceTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')
		self.project = Project.objects.create(
			title='some project', description='some description',
			category=self.category, user=self.user, pinned=True
		)

	def test_unpin_with_pinned_project(self):
		resp = unpin_project(self.project.pk)
		project = Project.objects.get(pk=self.project.pk)
		self.assertFalse(project.pinned)
		self.assertEqual(resp, {'unpinned': True})

	def test_pin_with_already_not_pinned_project(self):
		self.project.pinned = False
		self.project.save()
		resp = unpin_project(self.project.pk)
		project = Project.objects.get(pk=self.project.pk)
		self.assertFalse(project.pinned)
		self.assertEqual(resp, {'unpinned': False})


class SearchProjectsServiceTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')
		self.project = Project.objects.create(
			title='some project', description='some description',
			category=self.category, user=self.user, pinned=True
		)

	def test_search(self):
		service = SearchProjectsService()
		projects = service.search(
			category=[self.category.pk], query=['some project']
		)
		self.assertEqual(projects.count(), 1)
		self.assertEqual(projects[0], self.project)

	def test_search_with_incorrect_parameters(self):
		service = SearchProjectsService()
		projects = service.search(parameter=['value'])
		self.assertEqual(projects.count(), 1)
		self.assertEqual(projects[0], self.project)

	def test_search_with_not_existing_category(self):
		service = SearchProjectsService()
		projects = service.search(category=[uuid4()])
		self.assertEqual(projects.count(), 0)

	def test_search_with_not_existing_query(self):
		service = SearchProjectsService()
		projects = service.search(query='query')
		self.assertEqual(projects.count(), 0)
