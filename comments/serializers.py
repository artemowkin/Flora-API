from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
	"""Project comment serializer"""

	user = serializers.CharField(source='user.username', read_only=True)

	class Meta:
		model = Comment
		fields = ('pk', 'reply_on', 'user', 'text', 'pub_datetime')
		read_only_fields = ('pk', 'user', 'pub_datetime')
