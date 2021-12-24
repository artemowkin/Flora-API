from typing import Union
from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from projects.models import Project


def get_project_comments(project_pk: Union[UUID,str]) -> QuerySet:
	"""Return comments on project"""
	project = get_object_or_404(Project, pk=project_pk)
	return project.comments.all()
