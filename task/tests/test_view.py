from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from task.models import Task, Tag
from task.serializers import TaskSerializer, CustomTagField


class TaskAPITestCase(APITestCase):
    tags = CustomTagField(many=True)

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)
        self.tag = Tag.objects.create(name="Sample Tag")
        self.task_data = {
            "title": "Test Task",
            "description": "Sample description",
            "due_date": "2023-12-31",
            "tags": ["Sample Tag"],
            "status": "OPEN",
        }

    def test_create_task(self):
        response = self.client.post("/api/tasks/", self.task_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response.data.pop("id")
        response.data.pop("timestamp")
        self.assertEqual(response.data, self.task_data)

    def test_retrieve_task(self):
        serializer = TaskSerializer(data=self.task_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        serializer_data_id = serializer.data["id"]
        response = self.client.get(f"/api/tasks/{serializer_data_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {**serializer.data})

    def test_retrieve_all_task(self):
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_task(self):
        serializer = TaskSerializer(data=self.task_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        serializer_data_id = serializer.data["id"]
        updated_data = {"title": "Updated Task", "status": "DONE", "tags": ["UPD Tag"]}
        response = self.client.put(f"/api/tasks/{serializer_data_id}/", updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=serializer_data_id)
        serializer = TaskSerializer(task)
        self.assertEqual(serializer.data["title"], updated_data["title"])
        self.assertEqual(serializer.data["status"], updated_data["status"])
        self.assertEqual(serializer.data["tags"], updated_data["tags"])

    def test_delete_task(self):
        serializer = TaskSerializer(data=self.task_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        serializer_data_id = serializer.data["id"]
        response = self.client.delete(f"/api/tasks/{serializer_data_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_get_nonexistent_task(self):
        response = self.client.get("/api/tasks/100000000000000000/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error_message = '{"error":"Task with id = 100000000000000000 not found."}'
        self.assertEqual(response.content.decode(), expected_error_message)

    def test_update_nonexistent_task(self):
        updated_data = {"title": "Updated Task", "status": "DONE", "tags": ["UPD Tag"]}
        response = self.client.put("/api/tasks/100000000000000000/", updated_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error_message = '{"error":"Task with id = 100000000000000000 not found."}'
        self.assertEqual(response.content.decode(), expected_error_message)

    def test_delete_nonexistent_task(self):
        response = self.client.delete("/api/tasks/100000000000000000/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error_message = '{"error":"Task with id = 100000000000000000 not found."}'
        self.assertEqual(response.content.decode(), expected_error_message)

    def test_illegal_task_creation(self):
        self.task_data["Illegal_item"] = "Illegal Item"
        response = self.client.post("/api/tasks/", self.task_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"message": "Request body contains illegal elements"})

    def test_illegal_task_updation(self):
        serializer = TaskSerializer(data=self.task_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        serializer_data_id = serializer.data["id"]
        updated_data = {
            "title": "Updated Task",
            "status": "DONE",
            "tags": ["UPD Tag"],
            "Illegal_item": "Illegal Item",
        }
        response = self.client.put(f"/api/tasks/{serializer_data_id}/", updated_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"message": "Request body contains illegal elements"})

    def test_task_creation_validation_error(self):
        self.task_data["due_date"] = "2000-07-15"
        response = self.client.post("/api/tasks/", self.task_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error_message = '{"error":"Due Date cannot be before Timestamp created."}'
        self.assertEqual(response.content.decode(), expected_error_message)

    def test_task_updation_validation_error(self):
        serializer = TaskSerializer(data=self.task_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        serializer_data_id = serializer.data["id"]
        updated_data = {
            "title": "Updated Task",
            "status": "DONE",
            "tags": ["UPD Tag"],
            "due_date": "2000-07-15",
        }
        response = self.client.put(f"/api/tasks/{serializer_data_id}/", updated_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error_message = '{"error":"Due Date cannot be before Timestamp created."}'
        self.assertEqual(response.content.decode(), expected_error_message)


class TagAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)
        self.tag_data = {"name": "New Tag"}

    def test_get_tags(self):
        response = self.client.get("/api/tags/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_tag(self):
        response = self.client.post("/api/tags/", self.tag_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 1)

    def test_retrieve_tag(self):
        tag = Tag.objects.create(name="Sample Tag")
        response = self.client.get(f"/api/tags/{tag.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tag.name, "Sample Tag")

    def test_update_tag(self):
        tag = Tag.objects.create(name="Sample Tag")
        updated_data = {"name": "Updated Tag"}
        response = self.client.put(f"/api/tags/{tag.id}/", updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, "Updated Tag")

    def test_delete_tag(self):
        tag = Tag.objects.create(name="Sample Tag")
        response = self.client.delete(f"/api/tags/{tag.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tag.objects.count(), 0)

    def test_create_invalid_tag(self):
        invalid_data = {"invalid_field": "value"}
        response = self.client.post("/api/tags/", invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error_message = '{"name":["This field is required."]}'
        self.assertIn(expected_error_message, response.content.decode())

    def test_get_nonexistent_tag(self):
        response = self.client.get("/api/tags/100000000000000000/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error_message = '{"error":"Tag with id = 100000000000000000 not found."}'
        self.assertEqual(response.content.decode(), expected_error_message)

    def test_update_nonexistent_tag(self):
        response = self.client.put("/api/tags/100000000000000000/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error_message = '{"error":"Tag with id = 100000000000000000 not found."}'
        self.assertEqual(response.content.decode(), expected_error_message)

    def test_delete_nonexistent_tag(self):
        response = self.client.delete("/api/tags/100000000000000000/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error_message = '{"error":"Tag with id = 100000000000000000 not found."}'
        self.assertEqual(response.content.decode(), expected_error_message)

    def test_illegal_tag_updation(self):
        tag = Tag.objects.create(name="Sample Tag")
        updated_data = {"Illegal_item": "Illegal"}
        response = self.client.put(f"/api/tags/{tag.id}/", updated_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error_message = '{"name":["This field is required."]}'
        self.assertIn(expected_error_message, response.content.decode())
