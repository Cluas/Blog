from django.contrib import admin
from .models import Post, Category, Tag


class PostAdmin(admin.ModelAdmin):
    module = Post
    list_display = ["title", "author", "publish", "status"]
    list_filter = ["publish", "status"]
    search_fields = ("title", "body")
    date_hierarchy = "publish"
    ordering = ["status", "publish"]
    raw_id_fields = ("author",)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
