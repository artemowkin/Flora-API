from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services import like_project, unlike_project


class LikeProjectView(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request, pk):
		liked = like_project(pk, request.user)
		return Response({'liked': liked}, status=200)


class UnlikeProjectView(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request, pk):
		unliked = unlike_project(pk, request.user)
		return Response({'unliked': unliked}, status=200)
