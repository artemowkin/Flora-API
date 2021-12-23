from django.test import TestCase
from django.contrib.auth import get_user_model

from likes.models import Like
from ..models import Project, ProjectImage
from ..serializers import SimpleProjectSerializer, DetailProjectSerializer
from categories.models import Category


User = get_user_model()


class SimpleProjectSerializertestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')
		self.project = Project.objects.create(
			title='some project', description='some description',
			category=self.category, user=self.user
		)
		self.project_image = ProjectImage.objects.create(
			image='some_image.jpg', project=self.project
		)
		self.project_like = Like.objects.create(
			project=self.project, user=self.user
		)

	def test_serialized_project(self):
		serialized_project = SimpleProjectSerializer(
			self.project, context={'user': self.user}
		).data
		self.assertEqual(serialized_project, {
			'pk': str(self.project.pk),
			'preview': '/media/some_image.jpg',
			'title': 'some project',
			'likes': 1,
			'is_already_liked': True,
		})


class DetailProjectSerializerTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')
		self.project = Project.objects.create(
			title='some project', description='some description',
			category=self.category, user=self.user
		)
		self.project_image = ProjectImage.objects.create(
			image='some_image.jpg', project=self.project
		)
		self.project_like = Like.objects.create(
			user=self.user, project=self.project
		)
		project_pub_datetime = (
			self.project.pub_datetime.isoformat()[:-6] + 'Z'
		)
		self.project_data = {
			'pk': str(self.project.pk),
			'title': self.project.title,
			'description': self.project.description,
			'images': ['/media/some_image.jpg'],
			'pinned': False,
			'category': {
				'pk': str(self.category.pk),
				'title': self.category.title
			},
			'user': self.user.username,
			'views': 0,
			'likes': 1,
			'pub_datetime': project_pub_datetime,
		}

	def test_serialized_project(self):
		serialized_project = DetailProjectSerializer(self.project).data
		self.assertEqual(serialized_project, self.project_data)

	def test_is_data_valid(self):
		serializer = DetailProjectSerializer(data={
			'title': 'some title', 'description': 'some description',
			'category': self.category.pk
		})
		self.assertTrue(serializer.is_valid())
