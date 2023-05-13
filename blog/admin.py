from django.contrib import admin
from .models import Author,Post,Tag,Comments
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_filter = ("author","tags","date")
    list_display = ("title","date","author")

class CommentsAdmin(admin.ModelAdmin):
    list_display = ("user_name","post","text")
admin.site.register(Author)
admin.site.register(Post,PostAdmin)
admin.site.register(Tag)
admin.site.register(Comments,CommentsAdmin)
