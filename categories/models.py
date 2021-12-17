from uuid import uuid4

from django.db import models


class Category(models.Model):
	"""Project category model"""

	uuid = models.UUIDField(primary_key=True, unique=True, default=uuid4)
	title = models.CharField('category title', max_length=255)

	class Meta:
		db_table = 'categories'
		ordering = ('title',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.title
