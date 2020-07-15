from django.contrib import admin

from API.patreon.models.patreon import (PatreonImage, PatreonOption,
                                        PatreonUnlockedPublication, Survey)


class SurveyOptionInLine(admin.TabularInline):
    model = PatreonOption
    extra = 0


class SurveyAdmin(admin.ModelAdmin):
    inlines = (
        SurveyOptionInLine,
    )


admin.site.register(PatreonImage)
admin.site.register(PatreonUnlockedPublication)
admin.site.register(Survey, SurveyAdmin)
