from django.contrib import admin
from django.contrib.auth.models import User
from .models import News, Files, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'користувачі'
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'get_rank')

    def get_rank(self, instance):
		return instance.profile.rank

    get_rank.short_description = 'Rank'


class NewsAdmin(admin.ModelAdmin):
	list_display = ('title', 'content', 'photo')
	list_display_links = ('title',)


class FilesAdmin(admin.ModelAdmin):
	list_display = ('path', 'size', 'uploaded_at', 'username')
	list_display_links = ('username',)


admin.site.register(News, NewsAdmin)
admin.site.register(Files, FilesAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
