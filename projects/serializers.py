from rest_framework import serializers

from .models import Project, ProjectImage


class ProjectImageSerializer(serializers.ModelSerializer):
	"""Serializer for project image"""

	class Meta:
		model = ProjectImage
		fields = ('image',)


class ProjectSerializer(serializers.ModelSerializer):
	"""Serializer for project"""

	user = serializers.CharField(source='user.username', read_only=True)
	images = ProjectImageSerializer(read_only=True, many=True)

	class Meta:
		model = Project
		fields = (
			'pk', 'title', 'description', 'images', 'category', 'user',
			'pub_datetime'
		)
		read_only_fields = ('pk', 'user', 'images', 'pub_datetime')
