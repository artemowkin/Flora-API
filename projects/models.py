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
	pinned = models.BooleanField('is project pinned', default=False)
	category = models.ForeignKey(
		Category, on_delete=models.CASCADE, verbose_name='project category',
		related_name='projects'
	)
	user = models.ForeignKey(
		User, on_delete=models.CASCADE, verbose_name='project user',
		related_name='projects'
	)
	views = models.PositiveIntegerField(editable=False, default=0)
	pub_datetime = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'projects'
		ordering = ('pub_datetime',)
		verbose_name = 'project'
		verbose_name_plural = 'projects'

	def __str__(self):
		return self.title


class ProjectImage(models.Model):
	"""Image for project"""

	image = models.ImageField('project image', upload_to='projects')
	project = models.ForeignKey(
		Project, on_delete=models.CASCADE, related_name='images'
	)

	class Meta:
		db_table = 'project_images'
