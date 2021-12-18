from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator

from .services import ProjectCRUDFacade
from .serializers import ProjectSerializer


class AllCreateProjectsView(APIView):

	def dispatch(self, request, *args, **kwargs):
		self.project_crud = ProjectCRUDFacade(request.user)
		return super().dispatch(request, *args, **kwargs)

	def get(self, request):
		all_projects = self.project_crud.get_all()
		paginated_projects = self._paginate_projects(all_projects)
		serialized_projects = ProjectSerializer(
			paginated_projects, many=True
		).data
		return Response(serialized_projects)

	def _paginate_projects(self, all_projects):
		paginator = Paginator(all_projects, 20)
		page_number = self._get_page_number(paginator)
		page = paginator.page(page_number)
		return page.object_list

	def _get_page_number(self, paginator):
		page_number = self.request.GET.get('page', '1')
		if not page_number.isdigit() or int(page_number) < 1: return 1
		if int(page_number) > paginator.num_pages: return paginator.num_pages
		return int(page_number)
