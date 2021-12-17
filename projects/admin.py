from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	list_display = ('title', 'description', 'category', 'user')
	search_by = ('title', 'description')
	raw_id_fields = ('category', 'user')
