from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import Project, ProjectMember, Comment

User = get_user_model()


class ProjectListCreateViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123", username="TestUser"
        )
        self.client.force_authenticate(user=self.user)
        self.url = "/api/projects/"

    def test_list_projects(self):
        """Test listing projects where the user is a member."""
        project = Project.objects.create(name="Test Project", owner=self.user)
        ProjectMember.objects.create(user=self.user, project=project, role="owner")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Project")

    def test_create_project(self):
        """Test creating a new project."""
        payload = {
            "name": "New Project",
            "description": "A new project description",
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Project")
        self.assertTrue(Project.objects.filter(name="New Project").exists())


class ProjectDetailViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test1@example.com", password="testpass123", username="TestUser1"
        )
        self.project = Project.objects.create(name="Test Project", owner=self.user)
        ProjectMember.objects.create(user=self.user, project=self.project, role="owner")
        self.client.force_authenticate(user=self.user)
        self.url = f"/api/projects/{self.project.id}/"

    def test_retrieve_project(self):
        """Test retrieving a specific project."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Project")

    def test_update_project(self):
        """Test updating a project (only Editors and Owners)."""
        payload = {
            "name": "Updated Project",
        }
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Project")

    def test_delete_project(self):
        """Test deleting a project (only Owners)."""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())


class ProjectMemberViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="testpass123",
        )
        self.user = User.objects.create_user(
            username="user",
            email="user@example.com",
            password="testpass123",
        )
        self.project = Project.objects.create(name="Test Project", owner=self.owner)
        ProjectMember.objects.create(
            user=self.owner, project=self.project, role="owner"
        )
        self.client.force_authenticate(user=self.owner)
        self.url = f"/api/projects/{self.project.id}/members/"


class CommentListCreateViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.project = Project.objects.create(name="Test Project", owner=self.user)
        ProjectMember.objects.create(user=self.user, project=self.project, role="owner")
        self.client.force_authenticate(user=self.user)
        self.url = f"/api/projects/{self.project.id}/comments/"

    def test_create_comment(self):
        """Test creating a comment (only Owners and Editors)."""
        payload = {
            "text": "This is a test comment.",
            "project": self.project.id,
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["text"], "This is a test comment.")

        # Clean up the created comment
        Comment.objects.filter(text="This is a test comment.").delete()
