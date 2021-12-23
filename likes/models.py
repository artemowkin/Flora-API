from django.db import models
from django.contrib.auth import get_user_model

from projects.models import Project


User = get_user_model()


class Like(models.Model):
	"""Project like model"""

	project = models.ForeignKey(
		Project, on_delete=models.CASCADE, related_name='likes'
	)
	user = models.ForeignKey(
		User, on_delete=models.CASCADE, related_name='likes'
	)

	class Meta:
		db_table = 'project_likes'
		constraints = [
			models.UniqueConstraint(
				name='unique_project_like', fields=('project', 'user')
			)
		]
