from uuid import UUID
from typing import Union

from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from projects.models import Project
from .models import Like


User = get_user_model()


def get_likes_count(likes: QuerySet) -> int:
	"""Return project likes count"""
	return likes.count()


def like_project(project_pk: Union[UUID,str], user: User) -> bool:
	"""Like project by user if not liked"""
	project = get_object_or_404(Project, pk=project_pk)
	like, created = Like.objects.get_or_create(project=project, user=user)
	if not created: return False
	return True


def is_already_liked(project: Project, user: User) -> bool:
	"""Is project already liked by user"""
	if not user.is_authenticated: return False
	try:
		Like.objects.get(project=project, user=user)
		return True
	except Like.DoesNotExist:
		return False
