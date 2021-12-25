from typing import Union, Optional
from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

from projects.models import Project
from .models import Comment


User = get_user_model()


def get_project_comments(project_pk: Union[UUID,str]) -> QuerySet:
	"""Return comments on project"""
	project = get_object_or_404(Project, pk=project_pk)
	return project.comments.all()


def delete_project_comment(project_pk: Union[UUID,str],
		comment_pk: Union[UUID,str]) -> None:
	"""Delete the concrete project comment"""
	comment = get_object_or_404(Comment, project__pk=project_pk, pk=comment_pk)
	comment.delete()


class CreateCommentService:
	"""Service to create a new project comment"""

	def __init__(self, user: User) -> None:
		if not user.is_authenticated: raise PermissionDenied
		self._user = user

	def create(self, project_pk: Union[UUID,str], text: str,
			reply_on: Optional[UUID] = None) -> Comment:
		"""Create a new project comment"""
		reply_on_comment = self._get_reply_on_comment(reply_on)
		project = get_object_or_404(Project, pk=project_pk)
		self._check_reply_on_comment_project(reply_on_comment, project)
		return Comment.objects.create(
			reply_on=reply_on_comment, project=project, user=self._user,
			text=text
		)

	def _get_reply_on_comment(self,
			comment_pk: Optional[UUID]) -> Optional[Comment]:
		"""Get reply on comment by pk or None if comment_pk is None"""
		if comment_pk:
			return get_object_or_404(Comment, pk=comment_pk)
		else:
			return None

	def _check_reply_on_comment_project(self, comment: Optional[UUID],
			project: Project) -> None:
		"""Check is reply on comment on the same project as creating comment"""
		if comment and not comment.project == project:
			raise ValueError
