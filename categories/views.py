from rest_framework.views import APIView
from rest_framework.response import Response

from .services import CategoryCRUDFacade
from .serializers import CategorySerializer


class BaseCategoryCRUDView(APIView):

	def dispatch(self, request, *args, **kwargs):
		self.category_crud = CategoryCRUDFacade(request.user)
		return super().dispatch(request, *args, **kwargs)


class AllCreateCategoriesView(BaseCategoryCRUDView):

	def get(self, request):
		all_categories = self.category_crud.get_all()
		serialized_categories = CategorySerializer(
			all_categories, many=True
		).data
		return Response(serialized_categories, status=200)
