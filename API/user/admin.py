from django.contrib import admin

from API.user.models.user import (Achievement, AchievementMembership, Border,
                                  BorderMembership, Preferences, TagFollow,
                                  Title, TitleMembership, User, UserFriendship)


class UserFollowInLine(admin.TabularInline):
    model = UserFriendship
    extra = 0
    fk_name = "follower"


class TagFollowInLine(admin.TabularInline):
    model = TagFollow
    extra = 0


class PreferencesInLine(admin.TabularInline):
    model = Preferences
    extra = 0


class TitleInLine(admin.TabularInline):
    model = TitleMembership
    extra = 0


class BorderTrueInLine(admin.TabularInline):
    model = Border
    extra = 0


class TitleAdmin(admin.ModelAdmin):
    exclude = ('user',)
    inlines = (
        BorderTrueInLine,
    )


class BorderInLine(admin.TabularInline):
    model = BorderMembership
    extra = 0


class BorderAdmin(admin.ModelAdmin):
    exclude = ('user',)


class AchievementInLine(admin.TabularInline):
    model = AchievementMembership
    extra = 0


class AchievementAdmin(admin.ModelAdmin):
    exclude = ('user',)


class UserAdmin(admin.ModelAdmin):
    exclude = ('groups', 'user_permissions',)
    inlines = (
        UserFollowInLine,
        TagFollowInLine,
        PreferencesInLine,
        AchievementInLine,
        BorderInLine,
        TitleInLine
    )


admin.site.register(Title, TitleAdmin)
admin.site.register(Border, BorderAdmin)
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Preferences)
