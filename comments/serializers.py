from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
	"""Project comment serializer"""

	user = serializers.CharField(source='user.username')

	class Meta:
		model = Comment
		fields = ('pk', 'reply_on', 'user', 'text', 'pub_datetime')
		read_only_fields = ('pk', 'username', 'pub_datetime')
