from django.test import TestCase
from django.contrib.auth import get_user_model

from ..services import get_likes_count
from ..models import Like
from projects.models import Project
from categories.models import Category


User = get_user_model()


class GetLikesCountServiceTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')
		self.project = Project.objects.create(
			title='some project', description='some description',
			category=self.category, user=self.user
		)
		self.like = Like.objects.create(project=self.project, user=self.user)

	def test_get_projects_like_count(self):
		self.assertEqual(get_likes_count(self.project.likes.all()), 1)
