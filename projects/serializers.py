from rest_framework import serializers
from django.conf import settings

from .models import Project, ProjectImage
from categories.models import Category


class CategoryField(serializers.Field):
	"""Field with category of project"""

	def to_representation(self, category):
		return str(category.title)

	def to_internal_value(self, category_pk):
		return Category.objects.get(pk=category_pk)


class ImagesField(serializers.Field):
	"""Field with many project images"""

	def to_representation(self, images):
		images_urls = [
			settings.MEDIA_URL + image_path[0]
			for image_path in images.values_list('image')
		]
		return images_urls


class ProjectSerializer(serializers.ModelSerializer):
	"""Serializer for project"""

	user = serializers.CharField(source='user.username', read_only=True)
	images = ImagesField(read_only=True)
	category = CategoryField()

	class Meta:
		model = Project
		fields = (
			'pk', 'title', 'description', 'images', 'category', 'user',
			'pub_datetime'
		)
		read_only_fields = ('pk', 'user', 'images', 'pub_datetime')
