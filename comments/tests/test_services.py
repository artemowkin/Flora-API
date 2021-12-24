from django.test import TestCase
from django.contrib.auth import get_user_model

from categories.models import Category
from projects.models import Project
from ..models import Comment
from ..services import get_project_comments


User = get_user_model()


class GetProjectCommentsServiceTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='Some category')
		self.project = Project.objects.create(
			title='Some project', description='Some description',
			category=self.category, user=self.user
		)
		self.comment = Comment.objects.create(
			project=self.project, user=self.user, text='some comment'
		)

	def test_get_project_comments(self):
		comments = get_project_comments(self.project.pk)
		self.assertEqual(comments.count(), 1)
		self.assertEqual(comments[0], self.comment)

	def test_get_project_comments_without_comments(self):
		new_project = Project.objects.create(
			title='Some project', description='Some description',
			category=self.category, user=self.user
		)
		comments = get_project_comments(new_project.pk)
		self.assertEqual(comments.count(), 0)
