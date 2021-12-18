from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.core.exceptions import PermissionDenied

from .models import Project
from categories.models import Category


User = get_user_model()


class GetProjectsService:
	"""Service to get projects entries"""

	def __init__(self) -> None:
		self._model = Project

	def get_all(self) -> QuerySet:
		"""Return all projects entries"""
		all_projects = self._model.objects.all()
		return all_projects


class CreateProjectService:
	"""Service to create a new project entry"""

	def __init__(self, user: User) -> None:
		if not user.is_staff: raise PermissionDenied
		self._user = user
		self._model = Project

	def create(self, title: str, description: str,
			category: Category) -> Project:
		"""Create a new project entry with title, description, and category"""
		project = self._model.objects.create(
			title=title, description=description, category=category,
			user=self._user
		)
		return project


class ProjectCRUDFacade:
	"""Facade with CRUD functionality for project"""

	def __init__(self, user: User) -> None:
		self._user = user
		self._get_projects_service = GetProjectsService()

	def get_all(self) -> QuerySet:
		"""Return all projects entries"""
		return self._get_projects_service.get_all()
