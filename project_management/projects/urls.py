from django.urls import path
from .views import ProjectListCreateView, ProjectDetailView, get_csrf_token, ProjectMemberView, CommentListCreateView

urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:project_id>/', ProjectDetailView.as_view(), name='project-detail'),
    path('csrf/', get_csrf_token, name='csrf_token'),
    path('projects/<int:project_id>/members/', ProjectMemberView.as_view(), name='project-member-add'),
    path('projects/<int:project_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
]
