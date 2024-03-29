from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
	"""Serializer for Category model"""

	class Meta:
		model = Category
		fields = ('pk', 'title')
		read_only_fields = ('pk',)
