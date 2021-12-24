from rest_framework.views import APIView
from rest_framework.response import Response

from .services import get_project_comments
from .serializers import CommentSerializer


class ProjectCommentsView(APIView):

	def get(self, request, pk):
		comments = get_project_comments(pk)
		serialized_comments = CommentSerializer(comments, many=True).data
		return Response(serialized_comments, status=200)
