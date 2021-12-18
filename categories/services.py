from uuid import UUID
from typing import Union

from django.shortcuts import get_object_or_404

from .models import Category


class GetCategoriesService:
	"""Service to get categories entries"""

	def __init__(self):
		self._model = Category

	def get_concrete(self, category_pk: Union[UUID,str]) -> Category:
		"""Return a concrete category using pk field. 404 if not found"""
		category = get_object_or_404(self._model, pk=category_pk)
		return category
