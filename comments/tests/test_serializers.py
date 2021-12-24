from django.test import TestCase
from django.contrib.auth import get_user_model

from categories.models import Category
from projects.models import Project
from ..models import Comment
from ..serializers import CommentSerializer


User = get_user_model()


class CommentSerializerTestCase(TestCase):

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

	def test_serialized_comment_fields(self):
		serialized_comment = CommentSerializer(self.comment).data
		self.assertEqual(serialized_comment['pk'], str(self.comment.pk))
		self.assertIsNone(serialized_comment['reply_on'])
		self.assertEqual(serialized_comment['user'], self.user.username)
		self.assertEqual(serialized_comment['text'], self.comment.text)
		self.assertIn('pub_datetime', serialized_comment)

	def test_reply_on_field(self):
		new_comment = Comment.objects.create(
			project=self.project, user=self.user, text='second comment',
			reply_on=self.comment
		)
		serialized_comment = CommentSerializer(new_comment).data
		self.assertEqual(serialized_comment['reply_on'], self.comment.pk)

	def test_is_data_valid_without_reply_on(self):
		data = {
			'project': str(self.project.pk), 'user': self.user.id,
			'text': 'some comment'
		}
		serializer = CommentSerializer(data=data)
		self.assertTrue(serializer.is_valid())

	def test_is_data_valid_with_reply_on(self):
		data = {
			'project': str(self.project.pk), 'user': self.user.id,
			'text': 'some comment', 'reply_on': str(self.comment.pk)
		}
		serializer = CommentSerializer(data=data)
		self.assertTrue(serializer.is_valid())
