from uuid import uuid4

from django.test import TestCase
from django.http import Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied

from ..models import Category
from ..services import (
	GetCategoriesService, CreateCategoryService, UpdateCategoryService,
	DeleteCategoryService
)


User = get_user_model()


class GetCategoriesServiceTestCase(TestCase):

	def setUp(self):
		self.category = Category.objects.create(title='some category')
		self.service = GetCategoriesService()

	def test_get_concrete_with_correct_pk(self):
		category = self.service.get_concrete(self.category.pk)
		self.assertEqual(category, self.category)

	def test_get_concrete_with_unexisting_pk(self):
		with self.assertRaises(Http404):
			category = self.service.get_concrete(uuid4())

	def test_get_all(self):
		categories = self.service.get_all()
		self.assertEqual(categories.count(), 1)
		self.assertEqual(categories[0], self.category)


class CreateCategoryServiceTestCase(TestCase):

	def setUp(self):
		self.category = Category.objects.create(title='some category')
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)

	def test_create_with_admin_user(self):
		service = CreateCategoryService(self.user)
		new_category = service.create(title='new category')
		self.assertEqual(Category.objects.count(), 2)
		self.assertEqual(new_category.title, 'new category')

	def test_create_with_not_authenticated_user(self):
		with self.assertRaises(PermissionDenied):
			CreateCategoryService(AnonymousUser())

	def test_create_with_simple_user(self):
		simple_user = User.objects.create_user(
			username='simpleuser', password='simplepass'
		)
		with self.assertRaises(PermissionDenied):
			CreateCategoryService(simple_user)


class UpdateCategoryServiceTestCase(TestCase):

	def setUp(self):
		self.category = Category.objects.create(title='some category')
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)

	def test_update(self):
		service = UpdateCategoryService(self.user)
		category = service.update(self.category.pk, 'new category title')
		self.assertEqual(category.pk, self.category.pk)
		self.assertEqual(category.title, 'new category title')

	def test_update_with_not_authenticated_user(self):
		with self.assertRaises(PermissionDenied):
			UpdateCategoryService(AnonymousUser())

	def test_update_with_simple_user(self):
		simple_user = User.objects.create_user(
			username='simpleuser', password='testpass'
		)
		with self.assertRaises(PermissionDenied):
			UpdateCategoryService(simple_user)


class DeleteCategoryServiceTestCase(TestCase):

	def setUp(self):
		self.category = Category.objects.create(title='some category')
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)

	def test_delete(self):
		service = DeleteCategoryService(self.user)
		category = service.delete(self.category.pk)
		self.assertEqual(Category.objects.count(), 0)

	def test_delete_with_not_authenticated_user(self):
		with self.assertRaises(PermissionDenied):
			DeleteCategoryService(AnonymousUser())

	def test_delete_with_simple_user(self):
		simple_user = User.objects.create_user(
			username='simpleuser', password='testpass'
		)
		with self.assertRaises(PermissionDenied):
			DeleteCategoryService(simple_user)
