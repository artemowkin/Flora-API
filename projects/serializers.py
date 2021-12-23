from rest_framework import serializers

from .models import Project, ProjectImage
from categories.services import GetCategoriesService
from likes.services import get_likes_count
from .services import get_project_images_urls, get_project_preview_url


class CategoryField(serializers.Field):
	"""Field with category of project"""

	def to_representation(self, category):
		return {'pk': str(category.pk), 'title': category.title}

	def to_internal_value(self, category_pk):
		service = GetCategoriesService()
		return service.get_concrete(category_pk)


class ImagesField(serializers.Field):
	"""Field with many project images"""

	def to_representation(self, images):
		return get_project_images_urls(images.all())


class ProjectPreviewField(serializers.Field):
	"""Field with project first image url"""

	def to_representation(self, images):
		return get_project_preview_url(images.all())


class LikesField(serializers.Field):
	"""Field with project likes count"""

	def to_representation(self, likes):
		return get_likes_count(likes.all())


class SimpleProjectSerializer(serializers.ModelSerializer):
	"""Serializer using in list of projects with simple necessary data"""

	preview = ProjectPreviewField(source='images', read_only=True)
	likes = LikesField(read_only=True)

	class Meta:
		model = Project
		fields = ('pk', 'title', 'preview', 'likes')
		read_only_fields = ('pk', 'title', 'preview', 'likes')


class DetailProjectSerializer(serializers.ModelSerializer):
	"""Serializer for project"""

	user = serializers.CharField(source='user.username', read_only=True)
	images = ImagesField(read_only=True)
	category = CategoryField()
	likes = LikesField(read_only=True)

	class Meta:
		model = Project
		fields = (
			'pk', 'title', 'description', 'images', 'pinned', 'category',
			'user', 'views', 'likes', 'pub_datetime'
		)
		read_only_fields = (
			'pk', 'user', 'images', 'pub_datetime', 'pinned', 'likes', 'views'
		)
