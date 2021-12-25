from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AnonymousUser

from categories.models import Category
from projects.models import Project
from ..models import Comment
from ..services import get_project_comments, CreateCommentService


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


class CreateProjectCommentServiceTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='Some category')
		self.project = Project.objects.create(
			title='Some project', description='Some description',
			category=self.category, user=self.user
		)
		self.create_comment_service = CreateCommentService(self.user)

	def test_create_without_reply_on(self):
		comment = self.create_comment_service.create(
			project_pk=self.project.pk, text='some comment'
		)
		self.assertIsNone(comment.reply_on)
		self.assertEqual(comment.project, self.project)
		self.assertEqual(comment.user, self.user)
		self.assertEqual(comment.text, 'some comment')
		self.assertEqual(self.project.comments.count(), 1)

	def test_create_with_reply_on(self):
		first_comment = self.create_comment_service.create(
			project_pk=self.project.pk, text='some comment'
		)
		second_comment = self.create_comment_service.create(
			project_pk=self.project.pk, text='second comment',
			reply_on=first_comment.pk
		)
		self.assertEqual(second_comment.reply_on, first_comment)
		self.assertEqual(second_comment.project, self.project)
		self.assertEqual(second_comment.user, self.user)
		self.assertEqual(second_comment.text, 'second comment')
		self.assertEqual(self.project.comments.count(), 2)

	def test_create_with_reply_on_another_project_comment(self):
		new_project = Project.objects.create(
			title='New project', description='Some description',
			category=self.category, user=self.user
		)
		first_comment = self.create_comment_service.create(
			project_pk=new_project.pk, text='some comment'
		)
		with self.assertRaises(ValueError):
			second_comment = self.create_comment_service.create(
				project_pk=self.project.pk, text='second comment',
				reply_on=first_comment.pk
			)

	def test_create_with_not_authenticated_user(self):
		with self.assertRaises(PermissionDenied):
			CreateCommentService(AnonymousUser())
