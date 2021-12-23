from projects.models import Project


def get_likes_count(project: Project) -> int:
	"""Return project likes count"""
	return project.likes.count()
