from rest_framework.views import APIView
from rest_framework.response import Response

from .services import (
	get_project_comments, CreateCommentService, delete_project_comment
)
from .serializers import CommentSerializer


class ProjectCommentsView(APIView):

	def get(self, request, project_pk):
		comments = get_project_comments(project_pk)
		serialized_comments = CommentSerializer(comments, many=True).data
		return Response(serialized_comments, status=200)

	def post(self, request, project_pk):
		serializer = CommentSerializer(data=request.data)
		if serializer.is_valid():
			try:
				return self._create_comment(project_pk)
			except ValueError:
				return self._handle_create_value_error()

		return Response(serializer.errors, status=400)

	def _create_comment(self, project_pk):
		create_service = CreateCommentService(self.request.user)
		created_comment = create_service.create(
			project_pk=project_pk, **self.request.data
		)
		serialized_comment = CommentSerializer(created_comment).data
		return Response(serialized_comment, status=201)

	def _handle_create_value_error(self):
		return Response({
			'detail': "You can't reply on comment on not the same project"
		}, status=400)


class DeleteProjectCommentView(APIView):

	def delete(self, request, project_pk, comment_pk):
		delete_project_comment(project_pk, comment_pk)
		return Response(status=204)
