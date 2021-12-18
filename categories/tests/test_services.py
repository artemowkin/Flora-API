from uuid import uuid4

from django.test import TestCase
from django.http import Http404

from ..models import Category
from ..services import GetCategoriesService


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
