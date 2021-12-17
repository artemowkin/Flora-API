from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model

from categories.models import Category


User = get_user_model()


class Project(models.Model):
	"""Art project model"""

	uuid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
	title = models.CharField('project title', max_length=255)
	description = models.TextField('project description')
	category = models.ForeignKey(
		Category, on_delete=models.CASCADE, verbose_name='project category'
	)
	user = models.ForeignKey(
		User, on_delete=models.CASCADE, verbose_name='project user'
	)
	pub_datetime = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'projects'
		ordering = ('pub_datetime',)
		verbose_name = 'project'
		verbose_name_plural = 'projects'

	def __str__(self):
		return self.title
