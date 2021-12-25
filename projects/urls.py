from django.urls import path

from . import views
from likes import views as likes_views
from comments import views as comments_views


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
	path('pinned/', views.PinnedProjectsView.as_view(), name='pinned_projects'),
	path('<uuid:pk>/pin/', views.PinProjectView.as_view(), name='pin_project'),
	path(
		'<uuid:pk>/unpin/', views.UnpinProjectView.as_view(),
		name='unpin_project'
	),
	path(
		'<uuid:pk>/like/', likes_views.LikeProjectView.as_view(),
		name='like_project'
	),
	path(
		'<uuid:pk>/unlike/', likes_views.UnlikeProjectView.as_view(),
		name='unlike_project'
	),
	path(
		'<uuid:pk>/comments/', comments_views.ProjectCommentsView.as_view(),
		name='project_comments'
	),
	path(
		'<uuid:pk>/comments/<uuid:comment_pk>/',
		comments_views.DeleteProjectCommentView.as_view(),
		name='delete_project_comment'
	),
]
