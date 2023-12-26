from django.test import TestCase
from task.models import Tag
from task.serializers import TaskSerializer, CustomTagField


class TaskSerializerTest(TestCase):
    tags = CustomTagField(many=True)

    def setUp(self):
        self.tag = Tag.objects.create(name="Sample Tag")

    def test_get_queryset(self):
        tag1 = Tag.objects.create(name="Tag1")
        tag2 = Tag.objects.create(name="Tag2")
        custom_tag_field = CustomTagField()
        queryset = custom_tag_field.get_queryset()
        self.assertIn(tag1, queryset)
        self.assertIn(tag2, queryset)

    def test_task_serializer(self):
        task_data = {
            "title": "Test Task",
            "description": "Sample description",
            "due_date": "2023-12-31",
            "tags": ["Urgent2", "Test7"],
            "status": "OPEN",
        }
        serializer = TaskSerializer(data=task_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(serializer.data["title"], "Test Task")
        self.assertEqual(serializer.data["description"], "Sample description")
        self.assertEqual(serializer.data["due_date"], "2023-12-31")
        self.assertEqual(serializer.data["status"], "OPEN")
        expected_tags = set(task_data["tags"])
        actual_tags = set(tag for tag in serializer.data["tags"])
        self.assertEqual(expected_tags, actual_tags)
