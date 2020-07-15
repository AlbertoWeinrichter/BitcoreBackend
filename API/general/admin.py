from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token

from API.general.models.general import CustomTag

admin.autodiscover()


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'count')


admin.site.register(CustomTag, TagAdmin)
admin.site.unregister(Group)
admin.site.unregister(Token)
