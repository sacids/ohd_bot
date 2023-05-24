from django.contrib import admin
from .models import Thread, SubThread, ThreadLink

# Register your models here.
class SubThreadInline(admin.TabularInline):
    model = SubThread
    ordering = ("view_id", )
    extra = 0


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'label', 'db_flag']
    search_fields = ['title__startwith']
    ordering = ("block","-created_at", "-updated_at")
    inlines  = [SubThreadInline]


@admin.register(ThreadLink)
class ThreadLinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'thread', 'sub_thread', 'link']
    ordering = ("id",)
