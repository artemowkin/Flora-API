from uuid import UUID
from datetime import date

from django.test import TestCase
from django.contrib.auth import get_user_model

from categories.models import Category
from ..models import Project, ProjectImage


User = get_user_model()


class BaseProjectModelTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='Some category')
		self.project = Project.objects.create(
			title='Some project', description='Some description',
			category=self.category, user=self.user
		)


class ProjectModelTestCase(BaseProjectModelTestCase):

	def test_created_project_fields(self):
		self.assertIsInstance(self.project.pk, UUID)
		self.assertEqual(self.project.title, 'Some project')
		self.assertEqual(self.project.description, 'Some description')
		self.assertFalse(self.project.pinned)
		self.assertEqual(self.project.category, self.category)
		self.assertEqual(self.project.user, self.user)
		self.assertEqual(self.project.views, 0)
		self.assertEqual(self.project.pub_datetime.date(), date.today())

	def test_string_representation(self):
		self.assertEqual(str(self.project), 'Some project')

	def test_user_related_field(self):
		self.assertEqual(self.user.projects.count(), 1)
		self.assertEqual(self.user.projects.get(), self.project)

	def test_category_related_field(self):
		self.assertEqual(self.category.projects.count(), 1)
		self.assertEqual(self.category.projects.get(), self.project)


class ProjectImageModelTestCase(BaseProjectModelTestCase):

	def setUp(self):
		super().setUp()
		self.project_image = ProjectImage.objects.create(
			image='some_image.jpg', project=self.project
		)

	def test_created_project_fields(self):
		self.assertEqual(
			self.project_image.image.url, '/media/some_image.jpg'
		)
		self.assertEqual(self.project_image.project, self.project)
