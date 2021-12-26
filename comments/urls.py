from django.urls import path

from . import views


urlpatterns = [
	path('', views.ProjectCommentsView.as_view(), name='project_comments'),
	path(
		'<uuid:comment_pk>/', views.DeleteProjectCommentView.as_view(),
		name='delete_project_comment'
	),
]
