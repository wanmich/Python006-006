from django.contrib import admin

# Register your models here.

from .models import ShortComments


class ShortCommentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'stars', 'comment', 'cid']
    search_fields = ['id', 'stars', 'comment', 'cid']


admin.site.register(ShortComments, ShortCommentsAdmin)
