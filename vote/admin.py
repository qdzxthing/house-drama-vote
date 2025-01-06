from django.contrib import admin
from .models import VoteData

@admin.register(VoteData)
class VoteDataAdmin(admin.ModelAdmin):
    list_display = ('house', 'get_house_display', 'visitor_ip', 'creation_time', 'last_modified_time')
    list_filter = ('house', 'creation_time', 'last_modified_time')
    search_fields = ('visitor_ip',)
    ordering = ('-creation_time',)
    date_hierarchy = 'creation_time'

    def get_house_display(self, obj):
        return obj.get_house_display()
    get_house_display.short_description = 'House Name'

from django.contrib import admin

# 修改站点的标题和头部标题
admin.site.site_header = "House Drama Competition 2025 Voting"
admin.site.site_title = "House Drama Competition Admin"
admin.site.index_title = "Welcome to the Voting Administration"
