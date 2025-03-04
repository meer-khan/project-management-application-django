import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Project, ProjectMember, Comment
from .serializers import ProjectSerializer, ProjectMemberSerializer, CommentSerializer

logger = logging.getLogger(__name__)


class ProjectListCreateView(APIView):
    """Handles listing and creating projects."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """List projects where the user is a member."""
        logger.info(f"User {request.user.email} requested their project list.")
        projects = Project.objects.filter(members__user=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new project."""
        logger.info(f"User {request.user.email} is attempting to create a new project.")
        serializer = ProjectSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            logger.info(
                f"Project '{serializer.data['name']}' created by {request.user.email}."
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.warning(f"Project creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):
    """Handles retrieving, updating, and deleting a project."""

    def get_object(self, project_id, user):
        """Helper method to get the project if user has access."""
        project = get_object_or_404(Project, id=project_id)
        if not ProjectMember.objects.filter(user=user, project=project).exists():
            logger.warning(
                f"Unauthorized access attempt by {user.email} on project ID {project_id}."
            )
            return None  # User has no role in this project
        return project

    def get(self, request, project_id):
        """Retrieve a specific project."""
        project = self.get_object(project_id, request.user)
        if not project:
            return Response(
                {"error": "Access denied"}, status=status.HTTP_403_FORBIDDEN
            )

        logger.info(f"User {request.user.email} retrieved project ID {project_id}.")
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, project_id):
        """Update a project (only Editors and Owners)."""
        project = self.get_object(project_id, request.user)
        if not project:
            return Response(
                {"error": "Access denied"}, status=status.HTTP_403_FORBIDDEN
            )

        member = ProjectMember.objects.filter(
            user=request.user, project=project
        ).first()
        if member.role not in ["owner", "editor"]:
            logger.warning(
                f"Permission denied: {request.user.email} attempted to update project ID {project_id}."
            )
            return Response(
                {"error": "You do not have permission to update this project."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Project ID {project_id} updated by {request.user.email}.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id):
        """Delete a project (only Owners)."""
        project = self.get_object(project_id, request.user)
        if not project:
            return Response(
                {"error": "Access denied"}, status=status.HTTP_403_FORBIDDEN
            )

        if project.owner != request.user:
            logger.warning(
                f"Unauthorized delete attempt on project ID {project_id} by {request.user.email}."
            )
            return Response(
                {"error": "Only the owner can delete this project."},
                status=status.HTTP_403_FORBIDDEN,
            )

        project.delete()
        logger.info(f"Project ID {project_id} deleted by {request.user.email}.")
        return Response(
            {"message": "Project deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProjectMemberView(APIView):
    """Allows project owners to add members."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, project_id):
        """Assign a role to a user (Only Owners)."""
        project = get_object_or_404(Project, id=project_id)
        if project.owner != request.user:
            logger.warning(
                f"Unauthorized role assignment attempt by {request.user.email} on project ID {project_id}."
            )
            return Response(
                {"error": "Only owners can assign roles."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProjectMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            logger.info(
                f"User {serializer.validated_data['user']} added to project ID {project_id} by {request.user.email}."
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.warning(f"Failed to add project member: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListCreateView(APIView):
    """Allows Owners & Editors to comment."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, project_id):
        """Create a comment on a project."""
        project = get_object_or_404(Project, id=project_id)
        member = ProjectMember.objects.filter(
            user=request.user, project=project
        ).first()

        if not member or member.role not in ["owner", "editor"]:
            logger.warning(
                f"Unauthorized comment attempt by {request.user.email} on project ID {project_id}."
            )
            return Response(
                {"error": "You do not have permission to comment."}, status=403
            )

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.warning(f"Comment creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, project_id):
        """List all comments for a project."""
        comments = Comment.objects.filter(project_id=project_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_csrf_token(request):
    return JsonResponse({"csrfToken": get_token(request)})
