from django.db.models import QuerySet


def get_likes_count(likes: QuerySet) -> int:
	"""Return project likes count"""
	return likes.count()
