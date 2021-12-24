from uuid import UUID

from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Comment
from projects.models import Project
from categories.models import Category


User = get_user_model()


class CommentModelTestCase(TestCase):

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

	def test_created_comment_fields(self):
		self.assertIsInstance(self.comment.pk, UUID)
		self.assertIsNone(self.comment.reply_on)
		self.assertEqual(self.comment.replies.count(), 0)
		self.assertEqual(self.comment.user, self.user)
		self.assertEqual(self.comment.project, self.project)
		self.assertEqual(self.comment.text, 'some comment')

	def test_comment_replies(self):
		reply_comment = Comment.objects.create(
			project=self.project, reply_on=self.comment, user=self.user,
			text='some reply comment'
		)
		self.assertEqual(self.comment.replies.get(), reply_comment)
