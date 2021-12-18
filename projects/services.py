from uuid import UUID
from typing import Union

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

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

	def get_concrete(self, project_pk: Union[UUID,str]) -> Project:
		"""Return a concrete project by pk"""
		concrete_project = get_object_or_404(self._model, pk=project_pk)
		return concrete_project


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

	def get_concrete(self, project_pk: Union[UUID,str]) -> Project:
		"""Return a concrete project"""
		return self._get_projects_service.get_concrete(project_pk)

	def create(self, title: str, description: str,
			category: Category) -> Project:
		"""Create a new project"""
		create_project_service = CreateProjectService(self._user)
		return create_project_service.create(title, description, category)
