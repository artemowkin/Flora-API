from django.db import models
from django.contrib.auth import get_user_model

from projects.models import Project


User = get_user_model()


class Comment(models.Model):
	"""Project comment model"""

	reply_on = models.ForeignKey(
		'self', on_delete=models.CASCADE, related_name='replies'
	)
	project = models.ForeignKey(
		Project, on_delete=models.CASCADE, related_name='comments'
	)
	user = models.ForeignKey(
		User, on_delete=models.CASCADE, related_name='comments'
	)
	text = models.TextField()
	pub_datetime = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'comments'
		ordering = ('-pub_datetime',)
