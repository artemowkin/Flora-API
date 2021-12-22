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


class ConcreteCategoryView(BaseCategoryCRUDView):

	def get(self, request, pk):
		category = self.category_crud.get_concrete(pk)
		serialized_category = CategorySerializer(category).data
		return Response(serialized_category, status=200)

	def put(self, request, pk):
		serializer = CategorySerializer(data=request.data)
		if serializer.is_valid():
			return self._serializer_valid(pk)

		return Response(serializer.errors, status=400)

	def _serializer_valid(self, pk):
		updated_category = self.category_crud.update(
			pk, self.request.data['title']
		)
		serialized_category = CategorySerializer(updated_category).data
		return Response(serialized_category, status=200)

	def delete(self, request, pk):
		self.category_crud.delete(pk)
		return Response(status=204)
