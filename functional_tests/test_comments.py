from django.contrib.auth import get_user_model
from django.test import TestCase

from categories.models import Category
from projects.models import Project
from comments.models import Comment


User = get_user_model()


class ProjectCommentsEndpointTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')
		self.project = Project.objects.create(
			title='some project', description='some description',
			category=self.category, user=self.user, pinned=True
		)
		self.comment = Comment.objects.create(
			user=self.user, project=self.project, text='some comment'
		)

	def test_get_all_comments(self):
		response = self.client.get(
			f'/api/v1/projects/{self.project.pk}/comments/'
		)
		self.assertEqual(response.status_code, 200)
		json_response = response.json()
		self.assertEqual(len(json_response), 1)
		json_comment = json_response[0]
		self.assertEqual(json_comment['pk'], str(self.comment.pk))
		self.assertEqual(json_comment['user'], self.user.username)
		self.assertEqual(json_comment['text'], self.comment.text)

	def test_create_a_new_project_comment_without_reply_on(self):
		self.client.login(username='testuser', password='testpass')
		response = self.client.post(
			f'/api/v1/projects/{self.project.pk}/comments/', {
				'text': 'new comment'
			}, content_type='application/json'
		)
		self.assertEqual(response.status_code, 201)
		json_response = response.json()
		self.assertEqual(Comment.objects.count(), 2)
		self.assertIn('pk', json_response)
		self.assertEqual(json_response['user'], self.user.username)
		self.assertEqual(json_response['text'], 'new comment')
		self.assertIsNone(json_response['reply_on'])

	def test_create_a_new_project_comment_with_reply_on(self):
		self.client.login(username='testuser', password='testpass')
		response = self.client.post(
			f'/api/v1/projects/{self.project.pk}/comments/', {
				'text': 'new comment', 'reply_on': str(self.comment.pk)
			}, content_type='application/json'
		)
		self.assertEqual(response.status_code, 201)
		json_response = response.json()
		self.assertEqual(Comment.objects.count(), 2)
		self.assertIn('pk', json_response)
		self.assertEqual(json_response['user'], self.user.username)
		self.assertEqual(json_response['text'], 'new comment')
		self.assertEqual(json_response['reply_on'], str(self.comment.pk))


class DeleteProjectCommentEndpointTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')
		self.project = Project.objects.create(
			title='some project', description='some description',
			category=self.category, user=self.user, pinned=True
		)
		self.comment = Comment.objects.create(
			user=self.user, project=self.project, text='some comment'
		)

	def test_delete_project_comment(self):
		self.client.login(username='testuser', password='testpass')
		response = self.client.delete(
			f'/api/v1/projects/{self.project.pk}/comments/{self.comment.pk}/'
		)
		self.assertEqual(response.status_code, 204)
