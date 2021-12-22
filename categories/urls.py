from django.urls import path

from . import views


urlpatterns = [
	path(
		'', views.AllCreateCategoriesView.as_view(),
		name='all_create_categories'
	),
]
