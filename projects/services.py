from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.core.exceptions import PermissionDenied

from .models import Project


User = get_user_model()


class GetProjectsService:
	"""Service to get projects entries"""

	def __init__(self) -> None:
		self._model = Project

	def get_all(self) -> QuerySet:
		"""Return all projects entries"""
		all_projects = self._model.objects.all()
		return all_projects
