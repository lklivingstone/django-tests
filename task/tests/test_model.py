from django.test import TestCase
from django.utils import timezone
from task.models import Tag, Task
from django.core.exceptions import ValidationError


class TaskModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Sample Tag")

    def test_tag_str_method(self):
        tag = Tag.objects.create(name="Test Tag")
        self.assertEqual(str(tag), "Test Tag")

    def test_task_str_method(self):
        task = Task(
            title="Test Task",
            description="Sample description",
            due_date=timezone.now().date() + timezone.timedelta(days=1),
            status="OPEN",
        )
        task.save()
        task.tags.add(self.tag)
        saved_task = Task.objects.get(pk=task.pk)
        self.assertEqual(str(saved_task), "Test Task")

    def test_task_due_date_validation(self):
        task = Task(
            title="Test Task",
            description="Sample description",
            due_date=timezone.now().date() - timezone.timedelta(days=1),
            status="OPEN",
        )
        with self.assertRaisesMessage(ValidationError, "Due Date cannot be before Timestamp created."):
            task.full_clean()

    def test_task_save(self):
        task = Task(
            title="Test Task",
            description="Sample description",
            due_date=timezone.now().date() + timezone.timedelta(days=1),
            status="OPEN",
        )

        task.save()
        task.tags.add(self.tag)
        saved_task = Task.objects.get(pk=task.pk)
        self.assertEqual(saved_task.description, "Sample description")
        self.assertEqual(saved_task.title, "Test Task")
        self.assertEqual(saved_task.due_date, task.due_date)
        self.assertEqual(saved_task.status, "OPEN")
        self.assertIn(self.tag, saved_task.tags.all())
