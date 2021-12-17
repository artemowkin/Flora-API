from uuid import UUID
from datetime import date

from django.test import TestCase
from django.contrib.auth import get_user_model

from categories.models import Category
from ..models import Project


User = get_user_model()


class ProjectModelTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='Some category')
		self.project = Project.objects.create(
			title='Some project', description='Some description',
			category=self.category, user=self.user
		)

	def test_created_project_fields(self):
		self.assertIsInstance(self.project.pk, UUID)
		self.assertEqual(self.project.title, 'Some project')
		self.assertEqual(self.project.description, 'Some description')
		self.assertEqual(self.project.category, self.category)
		self.assertEqual(self.project.user, self.user)
		self.assertEqual(self.project.pub_datetime.date(), date.today())

	def test_string_representation(self):
		self.assertEqual(str(self.project), 'Some project')
