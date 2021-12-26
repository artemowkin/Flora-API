import re
from uuid import UUID
from typing import Union

from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Q
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import Project, ProjectImage
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
		self._add_project_view(concrete_project)
		return concrete_project

	def _add_project_view(self, project: Project) -> None:
		"""Increment views for project"""
		project.views += 1
		project.save()


class BaseConcreteProjectService:
	"""Base service with concrete project logic"""

	def __init__(self, user: User) -> None:
		if not user.is_staff: raise PermissionDenied
		self._user = user
		self._model = Project


class CreateProjectService(BaseConcreteProjectService):
	"""Service to create a new project entry"""

	def create(self, title: str, description: str,
			category: Category) -> Project:
		"""Create a new project entry with title, description, and category"""
		project = self._model.objects.create(
			title=title, description=description, category=category,
			user=self._user
		)
		return project


class UpdateProjectService(BaseConcreteProjectService):
	"""Service to update a concrete project"""

	def update(self, project_pk: Union[UUID,str], title: str, description: str,
			category: Category) -> Project:
		"""Update a concrete project"""
		project = get_object_or_404(self._model, pk=project_pk)
		project.title = title
		project.description = description
		project.category = category
		project.save()
		return project


class DeleteProjectService(BaseConcreteProjectService):
	"""Service to delete a concrete project"""

	def delete(self, project_pk: Union[UUID,str]) -> None:
		"""Delete a concrete project"""
		project = get_object_or_404(self._model, pk=project_pk)
		project.delete()


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

	def update(self, project_pk: Union[UUID,str], title: str,
			description: str, category: Category) -> Project:
		"""Update a concrete project"""
		update_project_service = UpdateProjectService(self._user)
		return update_project_service.update(
			project_pk, title, description, category
		)

	def delete(self, project_pk: Union[UUID,str]) -> None:
		"""Delete a concrete project by pk"""
		delete_service = DeleteProjectService(self._user)
		delete_service.delete(project_pk)


class SearchProjectsService:
	"""Service to search projects by category and query"""

	def __init__(self):
		self._model = Project

	def search(self, **kwargs: dict) -> QuerySet:
		"""Search projects by kwargs"""
		kwargs = self._normalize_kwargs(kwargs)
		methods = self._get_kwargs_methods(kwargs)
		return self._run_chain(methods, kwargs)

	def _normalize_kwargs(self, kwargs: dict) -> dict:
		"""Make kwargs values not iterable"""
		if not self._is_kwargs_valid(kwargs):
			return {key: value[0] for key, value in kwargs.items()}

		return kwargs

	def _is_kwargs_valid(self, kwargs: dict) -> dict:
		"""Check is kwargs values not iterable"""
		return not all([
			isinstance(kwargs[key], list) for key in kwargs
		])

	def _get_kwargs_methods(self, kwargs: dict) -> list:
		"""Return list with methods names"""
		return [key for key in kwargs if hasattr(self, key)]

	def _run_chain(self, methods: list, kwargs: dict) -> QuerySet:
		"""Calls methods one by one and returns result queryset"""
		result_queryset = self._model.objects.all()
		for method_name in methods:
			method = getattr(self, method_name)
			result_queryset = method(result_queryset, kwargs[method_name])

		return result_queryset

	def category(self, queryset: QuerySet,
			category_pk: Union[UUID,str]) -> QuerySet:
		"""Filter projects by category"""
		if not self._is_uuid_valid(category_pk): return queryset
		return queryset.filter(category__pk=category_pk)

	def _is_uuid_valid(self, uuid: Union[UUID,str]) -> bool:
		"""Check is uuid valid"""
		if isinstance(uuid, UUID): return True
		uuid_regexp = r"[a-f0-9]{8}(-[a-f0-9]{4}){4}[a-f0-9]{8}"
		return re.match(uuid_regexp, uuid)

	def query(self, queryset: QuerySet, query_value: str) -> QuerySet:
		"""Search projects by query in title and description"""
		return queryset.filter(
			Q(title__icontains=query_value) |
			Q(description__icontains=query_value)
		)


def add_project_images(project: Project, images: list) -> None:
	"""Add images for project"""
	for image in images:
		ProjectImage.objects.create(project=project, image=image)


def get_project_images_urls(images: QuerySet) -> list:
	"""Return images urls list"""
	images_urls = [image_obj.image.url for image_obj in images]
	return images_urls


def get_project_preview_url(images: QuerySet) -> str:
	"""Return first project image url"""
	if not images: return ''
	first_image_url = images[0].image.url
	return first_image_url


def get_pinned_projects() -> QuerySet:
	"""Return pinned projects"""
	pinned_projects = Project.objects.filter(pinned=True)[:20:1]
	return pinned_projects


def pin_project(project_pk: Union[UUID,str]) -> dict:
	"""Pin project. If already pinned, do nothing"""
	project = get_object_or_404(Project, pk=project_pk)
	if project.pinned: return {'pinned': False}
	project.pinned = True
	project.save()
	return {'pinned': True}


def unpin_project(project_pk: Union[UUID,str]) -> dict:
	"""Unpin project. if already not pinned, do nothing"""
	project = get_object_or_404(Project, pk=project_pk)
	if not project.pinned: return {'unpinned': False}
	project.pinned = False
	project.save()
	return {'unpinned': True}
