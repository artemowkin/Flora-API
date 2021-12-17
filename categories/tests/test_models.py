from uuid import UUID

from django.test import TestCase

from ..models import Category


class CategoryModelTestCase(TestCase):

	def setUp(self):
		self.category = Category.objects.create(title='some category')

	def test_created_category_fields(self):
		self.assertIsInstance(self.category.pk, UUID)
		self.assertEqual(self.category.title, 'some category')

	def test_string_representation(self):
		self.assertEqual(str(self.category), 'some category')
