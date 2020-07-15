import tagulous.admin
from django.contrib import admin

from API.comments.models.comment import Comment
from API.publication.models.publication import (ProsAndCons, Publication,
                                                PublicationImage,
                                                PublicationScore)
from API.user.models.user import User


class PublicationImageInLine(admin.TabularInline):
    model = PublicationImage
    extra = 0


class ProsAndConsInLine(admin.TabularInline):
    model = ProsAndCons
    extra = 0


class PublicationScoreInLine(admin.TabularInline):
    model = PublicationScore
    extra = 0


class PublicationPostInLine(admin.TabularInline):
    model = Comment
    extra = 0


class PublicationAdmin(admin.ModelAdmin):
    inlines = [
        PublicationImageInLine,
        ProsAndConsInLine,
        PublicationScoreInLine,
        PublicationPostInLine
    ]

    # def get_inline_formsets(self, request, formsets, inline_instances, obj=None):
    #     print(formsets[0].data)
    #

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = User.objects.filter(is_staff=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


tagulous.admin.register(Publication, PublicationAdmin)
admin.register(Publication, PublicationAdmin)
