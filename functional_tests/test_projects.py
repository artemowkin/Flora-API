from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from likes.models import Like
from categories.models import Category
from projects.models import Project, ProjectImage


User = get_user_model()


class AllCreateProjectsEndpointTestCase(TestCase):

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

	def test_get_all_projects(self):
		response = self.client.get('/api/v1/projects/')
		self.assertEqual(response.status_code, 200)
		json = response.json()
		self.assertEqual(json, {
			'current_page': 1,
			'num_pages': 1,
			'projects': [{
				'pk': str(self.project.pk),
				'preview': '/media/some_image.jpg',
				'title': 'some project',
				'likes': 1
			}],
		})

	def test_pagination(self):
		for i in range(21):
			Project.objects.create(
				title=f'some project {i}', description='some description',
				category=self.category, user=self.user
			)

		response = self.client.get('/api/v1/projects/?page=1')
		json = response.json()
		self.assertEqual(len(json['projects']), 20)
		response = self.client.get('/api/v1/projects/?page=2')
		json = response.json()
		self.assertEqual(len(json['projects']), 2)

	def test_search(self):
		response = self.client.get(
			f'/api/v1/projects/?category={self.category.pk}'
			f'&query={self.project.title}'
		)
		self.assertEqual(response.status_code, 200)
		json_response = response.json()
		self.assertEqual(len(json_response['projects']), 1)
		self.assertEqual(
			json_response['projects'][0]['pk'], str(self.project.pk)
		)

	def test_create_with_not_authenticated_user(self):
		response = self._post_project()
		self.assertEqual(response.status_code, 403)

	def _post_project(self):
		return self.client.post('/api/v1/projects/', {
			'title': 'new project', 'description': 'some description',
			'category': self.category.pk
		}, content_type="application/json")

	def test_create_with_simple_user(self):
		simple_user = User.objects.create_user(
			username='simpleuser', password='testpass'
		)
		self.client.login(username='simpleuser', password='testpass')
		response = self._post_project()
		self.assertEqual(response.status_code, 403)

	def test_create_with_admin_user(self):
		self.client.login(username='testuser', password='testpass')
		response = self._post_project()
		self.assertEqual(response.status_code, 201)
		json_response = response.json()
		self.assertIn('pk', json_response)
		self.assertEqual(json_response['title'], 'new project')
		self.assertEqual(json_response['description'], 'some description')
		self.assertEqual(
			json_response['category']['title'], self.category.title
		)
		self.assertEqual(json_response['user'], self.user.username)
		self.assertEqual(json_response['images'], [])
		self.assertIn('pub_datetime', json_response)


class ConcreteProjectEndpointsTestCase(TestCase):

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

	def test_get_concrete_project(self):
		response = self.client.get(f'/api/v1/projects/{self.project.pk}/')
		self.assertEqual(response.status_code, 200)
		json_response = response.json()
		self.assertEqual(json_response['pk'], str(self.project.pk))
		self.assertEqual(json_response['title'], self.project.title)
		self.assertEqual(json_response['description'], self.project.description)
		self.assertEqual(json_response['user'], self.user.username)
		self.assertEqual(
			json_response['category']['title'], self.category.title
		)
		self.assertEqual(json_response['images'], ['/media/some_image.jpg'])
		self.assertEqual(json_response['views'], 1)

	def test_update_concrete_project(self):
		self.client.login(username='testuser', password='testpass')
		response = self.client.put(f'/api/v1/projects/{self.project.pk}/', {
			'title': 'new title', 'description': 'new description',
			'category': self.category.pk
		}, content_type='application/json')
		self.assertEqual(response.status_code, 200)
		json_response = response.json()
		self.assertEqual(json_response['pk'], str(self.project.pk))
		self.assertEqual(json_response['title'], 'new title')
		self.assertEqual(json_response['description'], 'new description')
		self.assertEqual(
			json_response['category']['title'], self.category.title
		)
		self.assertEqual(json_response['views'], 0)

	def test_delete_concrete_project(self):
		self.client.login(username='testuser', password='testpass')
		response = self.client.delete(f'/api/v1/projects/{self.project.pk}/')
		self.assertEqual(response.status_code, 204)
		self.assertEqual(Project.objects.count(), 0)


class PinnedProjectsEndpointTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')
		self.project = Project.objects.create(
			title='some project', description='some description',
			category=self.category, user=self.user
		)

	def test_get_pinned_projects(self):
		new_project = Project.objects.create(
			title='new project', description='some description',
			category=self.category, user=self.user, pinned=True
		)
		response = self.client.get('/api/v1/projects/pinned/')
		self.assertEqual(response.status_code, 200)
		json_response = response.json()
		self.assertEqual(len(json_response), 1)
		self.assertEqual(json_response[0]['title'], 'new project')


class PinProjectEndpointTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')
		self.project = Project.objects.create(
			title='some project', description='some description',
			category=self.category, user=self.user
		)

	def test_pin(self):
		self.client.login(username='testuser', password='testpass')
		response = self.client.post(f'/api/v1/projects/{self.project.pk}/pin/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(), {'pinned': True})


class UnpinProjectEndpointTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')
		self.project = Project.objects.create(
			title='some project', description='some description',
			category=self.category, user=self.user, pinned=True
		)

	def test_pin(self):
		self.client.login(username='testuser', password='testpass')
		response = self.client.post(
			f'/api/v1/projects/{self.project.pk}/unpin/'
		)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(), {'unpinned': True})


class LikeProjectEndpointTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.category = Category.objects.create(title='some category')
		self.project = Project.objects.create(
			title='some project', description='some description',
			category=self.category, user=self.user, pinned=True
		)

	def test_like_unliked_project(self):
		self.client.login(username='testuser', password='testpass')
		response = self.client.post(
			f'/api/v1/projects/{self.project.pk}/like/'
		)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(), {'liked': True})

	def test_like_already_liked_project(self):
		self.client.login(username='testuser', password='testpass')
		self.client.post(
			f'/api/v1/projects/{self.project.pk}/like/'
		)
		response = self.client.post(
			f'/api/v1/projects/{self.project.pk}/like/'
		)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(), {'liked': False})
