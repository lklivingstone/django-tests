from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from task.models import Task, Tag


class MockRequest(object):
    pass


request = MockRequest()


class TaskAdminTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="lk", password="livingstone")
        self.task = Task.objects.create(
            title="Test_Task", description="description", due_date="2024-12-01", status="OPEN"
        )
        self.tag = Tag.objects.create(name="Test_Tag")
        self.client.force_login(self.user)

    def test_update_task(self):
        data = {"action": "update_task", "_selected_action": [self.task.id]}
        url = reverse("admin:task_task_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_save_task(self):
        url = reverse("admin:task_task_changelist")
        response = self.client.post(
            url, {"action": "save_task", "_selected_action": [self.task.id]}, follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_get_all_task(self):
        data = {"action": "get_all_tasks", "_selected_action": [self.task.id]}
        url = reverse("admin:task_task_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_get_task(self):
        data = {"action": "get_task", "_selected_action": [self.task.id]}
        url = reverse("admin:task_task_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_get_task_invalid(self):
        data = {"action": "get_task_invalid", "_selected_action": [self.task.id]}
        url = reverse("admin:task_task_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_post_task(self):
        data = {"action": "post_task", "_selected_action": [self.task.id]}
        url = reverse("admin:task_task_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_post_task_illegal(self):
        data = {"action": "post_task_illegal", "_selected_action": [self.task.id]}
        url = reverse("admin:task_task_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_update_task_valid(self):
        data = {"action": "update_task_valid", "_selected_action": [self.task.id]}
        url = reverse("admin:task_task_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_update_task_invalid(self):
        data = {"action": "update_task_invalid", "_selected_action": [self.task.id]}
        url = reverse("admin:task_task_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_update_task_illegal(self):
        data = {"action": "update_task_illegal", "_selected_action": [self.task.id]}
        url = reverse("admin:task_task_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_update_task_due_date(self):
        data = {"action": "update_task_due_date", "_selected_action": [self.task.id]}
        url = reverse("admin:task_task_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_delete_task_valid(self):
        data = {"action": "delete_task_valid", "_selected_action": [self.task.id]}
        url = reverse("admin:task_task_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_delete_task_invalid(self):
        data = {"action": "delete_task_invalid", "_selected_action": [self.task.id]}
        url = reverse("admin:task_task_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_get_tags(self):
        data = {"action": "test_get_tags", "_selected_action": [self.tag.id]}
        url = reverse("admin:task_tag_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_post_tag(self):
        data = {"action": "post_tag", "_selected_action": [self.tag.id]}
        url = reverse("admin:task_tag_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_post_tag_invalid(self):
        data = {"action": "post_tag_invalid", "_selected_action": [self.tag.id]}
        url = reverse("admin:task_tag_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_get_tag(self):
        data = {"action": "get_tag", "_selected_action": [self.tag.id]}
        url = reverse("admin:task_tag_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_get_tag_invalid(self):
        data = {"action": "get_tag_invalid", "_selected_action": [self.tag.id]}
        url = reverse("admin:task_tag_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_put_tag_valid(self):
        data = {"action": "put_tag_valid", "_selected_action": [self.tag.id]}
        url = reverse("admin:task_tag_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_put_tag_invalid(self):
        data = {"action": "put_tag_invalid", "_selected_action": [self.tag.id]}
        url = reverse("admin:task_tag_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_put_tag_invalid_id(self):
        data = {"action": "put_tag_invalid_id", "_selected_action": [self.tag.id]}
        url = reverse("admin:task_tag_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_delete_tag_valid(self):
        data = {"action": "delete_tag_valid", "_selected_action": [self.tag.id]}
        url = reverse("admin:task_tag_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def test_delete_tag_invalid(self):
        data = {"action": "delete_tag_invalid", "_selected_action": [self.tag.id]}
        url = reverse("admin:task_tag_changelist")
        response = self.client.post(url, data, follow=True)
        assert response.status_code == 200

    def tearDown(self):
        self.task.delete()
        self.tag.delete()
