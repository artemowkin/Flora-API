from uuid import UUID

from django.test import TestCase
from django.db.utils import IntegrityError

from ..models import Category


class CategoryModelTestCase(TestCase):

	def setUp(self):
		self.category = Category.objects.create(title='some category')

	def test_created_category_fields(self):
		self.assertIsInstance(self.category.pk, UUID)
		self.assertEqual(self.category.title, 'some category')

	def test_string_representation(self):
		self.assertEqual(str(self.category), 'some category')

	def test_unique_title(self):
		with self.assertRaises(IntegrityError):
			Category.objects.create(title='some category')
