from rest_framework import serializers

from .models import Project, ProjectImage


class ProjectSerializer(serializers.ModelSerializer):
	"""Serializer for project"""

	user = serializers.CharField(source='user.username', read_only=True)

	class Meta:
		model = Project
		fields = (
			'pk', 'title', 'description', 'category', 'user',
			'pub_datetime'
		)
		read_only_fields = ('pk', 'user', 'pub_datetime')
