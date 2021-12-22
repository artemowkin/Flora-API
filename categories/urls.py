from django.urls import path

from . import views


urlpatterns = [
	path(
		'', views.AllCreateCategoriesView.as_view(),
		name='all_create_categories'
	),
	path(
		'<uuid:pk>/', views.ConcreteCategoryView.as_view(),
		name='concrete_category'
	),
]
