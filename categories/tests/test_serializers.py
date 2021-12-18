from django.test import TestCase

from ..models import Category
from ..serializers import CategorySerializer


class CategorySerializerTestCase(TestCase):

	def setUp(self):
		self.category = Category.objects.create(title='some category')
		self.category_data = {
			'pk': str(self.category.pk),
			'title': self.category.title,
		}

	def test_serialized_category(self):
		serialized_category = CategorySerializer(self.category).data
		self.assertEqual(serialized_category, self.category_data)

	def test_is_data_valid(self):
		serializer = CategorySerializer(data={'title': 'second category'})
		self.assertTrue(serializer.is_valid())
