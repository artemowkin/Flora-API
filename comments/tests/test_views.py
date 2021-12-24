from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from projects.models import Project
from categories.models import Category
from ..models import Comment


User = get_user_model()


class ProjectCommentsView(TestCase):

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

	def test_get(self):
		response = self.client.get(
			reverse('project_comments', args=[self.project.pk])
		)
		self.assertEqual(response.status_code, 200)
