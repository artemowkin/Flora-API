from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator

from .services import (
	ProjectCRUDFacade, add_project_images, GetProjectsService,
	pin_project, unpin_project, SearchProjectsService, get_pinned_projects
)
from .serializers import SimpleProjectSerializer, DetailProjectSerializer
from categories.services import GetCategoriesService


class BaseProjectCRUDView(APIView):

	def dispatch(self, request, *args, **kwargs):
		self.project_crud = ProjectCRUDFacade(request.user)
		return super().dispatch(request, *args, **kwargs)


class AllCreateProjectsView(BaseProjectCRUDView):

	def get(self, request):
		service = SearchProjectsService()
		projects = service.search(**request.GET)
		paginated_projects, page_obj = self._paginate_projects(projects)
		serialized_projects = self._serialize_projects(
			paginated_projects, page_obj
		)
		return Response(serialized_projects)

	def _paginate_projects(self, all_projects):
		paginator = Paginator(all_projects, 20)
		page_number = self._get_page_number(paginator)
		page = paginator.page(page_number)
		return page.object_list, page

	def _serialize_projects(self, projects, page):
		serialized_projects = SimpleProjectSerializer(
			projects, many=True, context={'user': self.request.user}
		).data
		return {
			'current_page': page.number, 'num_pages': page.paginator.num_pages,
			'projects': serialized_projects
		}

	def _get_page_number(self, paginator):
		page_number = self.request.GET.get('page', '1')
		if not page_number.isdigit() or int(page_number) < 1: return 1
		if int(page_number) > paginator.num_pages: return paginator.num_pages
		return int(page_number)

	def post(self, request):
		serializer = DetailProjectSerializer(data=request.data)
		if serializer.is_valid():
			project = self._create_project()
			serialized_project = DetailProjectSerializer(project).data
			return Response(serialized_project, status=201)

		return Response(serializer.errors, status=400)

	def _create_project(self):
		get_categories_service = GetCategoriesService()
		category = get_categories_service.get_concrete(
			self.request.data['category']
		)
		self.request.data.update({'category': category})
		return self.project_crud.create(**self.request.data)


class ConcreteProjectView(BaseProjectCRUDView):

	def dispatch(self, request, *args, **kwargs):
		self.project_crud = ProjectCRUDFacade(request.user)
		return super().dispatch(request, *args, **kwargs)

	def get(self, request, pk):
		project = self.project_crud.get_concrete(pk)
		serialized_project = DetailProjectSerializer(
			project, context={'user': request.user}
		).data
		return Response(serialized_project)

	def put(self, request, pk):
		serializer = DetailProjectSerializer(data=request.data)
		if serializer.is_valid():
			updated_project =  self._update_project(pk)
			serialized_project = self._serialize_project(updated_project)
			return Response(serialized_project, status=200)

		return Response(serializer.errors, status=400)

	def _serialize_project(self, project):
		return DetailProjectSerializer(
			project, context={'user': self.request.user}
		).data

	def _update_project(self, pk):
		get_categories_service = GetCategoriesService()
		category = get_categories_service.get_concrete(
			self.request.data['category']
		)
		self.request.data.update({'category': category})
		return self.project_crud.update(pk, **self.request.data)

	def delete(self, request, pk):
		self.project_crud.delete(pk)
		return Response(status=204)


class ProjectImagesUploadView(APIView):
	parser_classes = [MultiPartParser]

	def post(self, request, pk):
		images = [image for image in request.data.values()]
		add_project_images(pk, images)
		return Response(status=204)


class PinnedProjectsView(APIView):

	def get(self, request):
		pinned_projects = get_pinned_projects()
		serialized_projects = SimpleProjectSerializer(
			pinned_projects, many=True, context={'user': request.user}
		).data
		return Response(serialized_projects, status=200)


class PinProjectView(APIView):

	def post(self, request, pk):
		resp = pin_project(pk)
		return Response(resp, status=200)


class UnpinProjectView(APIView):

	def post(self, request, pk):
		resp = unpin_project(pk)
		return Response(resp, status=200)
