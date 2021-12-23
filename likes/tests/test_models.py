from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from projects.models import Project
from categories.models import Category
from ..models import Like


User = get_user_model()


class LikeModelTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')
		self.project = Project.objects.create(
			title='some project', description='some description',
			user=self.user, category=self.category
		)
		self.like = Like.objects.create(project=self.project, user=self.user)

	def test_created_like_attributes(self):
		self.assertEqual(self.like.user, self.user)
		self.assertEqual(self.like.project, self.project)
		self.assertEqual(self.project.likes.count(), 1)

	def test_project_user_unique_together_constraint(self):
		with self.assertRaises(IntegrityError):
			Like.objects.create(project=self.project, user=self.user)
