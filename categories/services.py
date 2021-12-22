from uuid import UUID
from typing import Union

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.core.exceptions import PermissionDenied

from .models import Category


User = get_user_model()


class GetCategoriesService:
	"""Service to get categories entries"""

	def __init__(self):
		self._model = Category

	def get_concrete(self, category_pk: Union[UUID,str]) -> Category:
		"""Return a concrete category using pk field. 404 if not found"""
		category = get_object_or_404(self._model, pk=category_pk)
		return category

	def get_all(self) -> QuerySet:
		"""Return all categories"""
		all_categories = self._model.objects.all()
		return all_categories


class BaseConcreteCategoryService:
	"""Base service with user checking"""

	def __init__(self, user: User) -> None:
		if not user.is_staff: raise PermissionDenied
		self._model = Category
		self._user = user


class CreateCategoryService(BaseConcreteCategoryService):
	"""Service to create a new category"""

	def create(self, title: str) -> Category:
		"""Create a new category entry using title"""
		category = Category.objects.create(title=title)
		return category


class UpdateCategoryService(BaseConcreteCategoryService):
	"""Service to update the concrete category"""

	def update(self, category_pk: Union[UUID,str], title: str) -> Category:
		"""Update the concrete category by pk"""
		category = get_object_or_404(self._model, pk=category_pk)
		category.title = title
		category.save()
		return category


class CategoryCRUDFacade:
	"""Facade with CRUD functionality for categories"""

	def __init__(self, user: User) -> None:
		self._user = user
		self._get_categories_service = GetCategoriesService()

	def get_concrete(self, category_pk: Union[UUID,str]) -> Category:
		"""Return a concrete category"""
		return self._get_categories_service.get_concrete(category_pk)

	def get_all(self) -> QuerySet:
		"""Return all categories"""
		return self._get_categories_service.get_all()

	def create(self, title: str) -> Category:
		"""Create a new category"""
		create_service = CreateCategoryService(self._user)
		return create_service.create(title)
