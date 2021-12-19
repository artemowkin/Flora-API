from django.urls import path

from . import views


urlpatterns = [
	path('', views.AllCreateProjectsView.as_view(), name='all_create_projects'),
	path(
		'<uuid:pk>/', views.ConcreteProjectView.as_view(),
		name='concrete_project'
	),
	path(
		'<uuid:pk>/upload_images/', views.ProjectImagesUploadView.as_view(),
		name='upload_project_images'
	),
]
