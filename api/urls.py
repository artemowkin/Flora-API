from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import PostViewSet, PostSearchView

router = SimpleRouter()
router.register('posts', PostViewSet)

urlpatterns = [
    path('posts/search/', PostSearchView.as_view()),
]

urlpatterns += router.urls
