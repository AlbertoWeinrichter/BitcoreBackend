import tagulous.admin
from django.contrib import admin

from .models.release import Release, ReleaseImage


class ReleaseImageInLine(admin.TabularInline):
    model = ReleaseImage
    extra = 0


class ReleaseAdmin(admin.ModelAdmin):
    inlines = [
        ReleaseImageInLine,
    ]

    def _projects(self, obj):
        return obj.projects.all().count()


admin.register(Release, ReleaseAdmin)
tagulous.admin.register(Release, ReleaseAdmin)
