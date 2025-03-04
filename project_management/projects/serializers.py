from rest_framework import serializers
from .models import Project, ProjectMember, Comment


class ProjectSerializer(serializers.ModelSerializer):
    """Handles project creation and details."""

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["owner", "created_at"]

    def create(self, validated_data):
        """Ensure the creator is the project owner."""
        user = self.context["request"].user
        validated_data.pop("owner", None)
        project = Project.objects.create(owner=user, **validated_data)
        ProjectMember.objects.create(user=user, project=project, role="owner")

        return project


class ProjectMemberSerializer(serializers.ModelSerializer):
    """Handles adding users to projects with roles."""

    class Meta:
        model = ProjectMember
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """Handles commenting on projects."""

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["user", "created_at"]
