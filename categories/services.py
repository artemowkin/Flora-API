from uuid import UUID
from typing import Union

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

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


class CategoryCRUDFacade:
	"""Facade with CRUD functionality for categories"""

	def __init__(self, user: User) -> None:
		self._user = user
		self._get_categories_service = GetCategoriesService()

	def get_concrete(self, category_pk: Union[UUID,str]) -> Category:
		"""Return a concrete category"""
		return self._get_categories_service.get_concrete(category_pk)
