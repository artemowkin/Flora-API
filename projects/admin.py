from django.contrib import admin

from .models import Project, ProjectImage


class ProjectImageInline(admin.TabularInline):
	model = ProjectImage


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	list_display = ('title', 'description', 'category', 'user')
	search_fields = ('title', 'description')
	raw_id_fields = ('category', 'user')
	inlines = (ProjectImageInline,)
