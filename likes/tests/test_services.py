from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from ..services import get_likes_count, like_project, is_already_liked
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


class LikeProjectServiceTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')
		self.project = Project.objects.create(
			title='some project', description='some description',
			category=self.category, user=self.user
		)

	def test_like_unliked_project(self):
		liked = like_project(self.project.pk, self.user)
		self.assertEqual(self.project.likes.count(), 1)
		self.assertTrue(liked)

	def test_like_already_liked_project(self):
		like_project(self.project.pk, self.user)
		liked = like_project(self.project.pk, self.user)
		self.assertFalse(liked)
		self.assertEqual(self.project.likes.count(), 1)


class IsAlreadyLikedServiceTestCase(TestCase):

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

	def test_check_is_alredy_liked_with_user_who_liked(self):
		liked = is_already_liked(self.project, self.user)
		self.assertTrue(liked)

	def test_check_is_already_liked_with_not_authenticated_user(self):
		liked = is_already_liked(self.project, AnonymousUser())
		self.assertFalse(liked)

	def test_check_is_already_liked_with_another_user(self):
		some_user = User.objects.create_user(
			username='newuser', password='testpass'
		)
		liked = is_already_liked(self.project, some_user)
		self.assertFalse(liked)
