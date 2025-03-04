from django.contrib import admin
from .models import Project, ProjectMember, Comment

class ProjectAdmin(admin.ModelAdmin):
    """Admin panel for projects."""
    
    list_display = ("id", "name", "owner", "created_at")  
    search_fields = ("name", "owner__username")  
    list_filter = ("created_at",)  
    ordering = ("-created_at",)

admin.site.register(Project, ProjectAdmin)


class ProjectMemberAdmin(admin.ModelAdmin):
    """Admin panel for managing project members."""
    
    list_display = ("id", "user", "project", "role")  
    search_fields = ("user__username", "project__name")  
    list_filter = ("role",)  

admin.site.register(ProjectMember, ProjectMemberAdmin)


class CommentAdmin(admin.ModelAdmin):
    """Admin panel for comments."""
    
    list_display = ("id", "user", "project", "text", "created_at")  
    search_fields = ("user__username", "project__name", "text")  
    list_filter = ("created_at",)  

admin.site.register(Comment, CommentAdmin)
