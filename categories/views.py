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

	def post(self, request):
		serializer = CategorySerializer(data=request.data)
		if serializer.is_valid():
			return self._serializer_valid()

		return Response(serializer.errors, status=400)

	def _serializer_valid(self):
		category = self.category_crud.create(**self.request.data)
		serialized_category = CategorySerializer(category).data
		return Response(serialized_category, status=201)
