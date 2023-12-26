from django.contrib import admin
from .models import Task, Tag
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory
import base64
from task.views import TaskRetrieveUpdateDestroyAPIView, TagListCreateAPIView
from django.test import Client
import json


class TaskAdmin(admin.ModelAdmin):
    list_filter = ["status", "due_date"]

    fieldsets = (
        ("Task Information", {"fields": ("title", "description", "due_date")}),
        ("Status", {"fields": ("status",)}),
        ("Additional Information", {"fields": ("tags",)}),
    )

    list_display = ("title", "status", "due_date", "timestamp", "id")
    list_editable = ("status", "due_date")

    def update_task(modeladmin, request, queryset):
        for task in queryset:
            factory = APIRequestFactory()
            url = reverse("task-retrieve", kwargs={"pk": task.id})
            invalid_data = {"title": "Test_Task_Updated", "due_date": "2020-12-12"}
            username = "lk"
            password = "livingstone"
            credentials = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")
            req = factory.put(
                url, data=invalid_data, format="json", HTTP_AUTHORIZATION=f"Basic {credentials}"
            )
            view = TaskRetrieveUpdateDestroyAPIView.as_view()
            try:
                view(req)
            except Exception:
                modeladmin.message_user(request, "Task Update Failed", level="ERROR")

    update_task.short_description = "Update Task"

    def save_task(modeladmin, request, queryset):
        for task in queryset:
            factory = APIRequestFactory()
            url = reverse("tasks-list-create")
            invalid_data = {
                "title": "Test_Task",
                "description": "description",
                "due_date": "2024-12-01",
                "tags": ["Test_Tag", "Test_Tag"],
                "status": "OPEN",
            }
            username = "lk"
            password = "livingstone"
            credentials = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")
            req = factory.post(
                url, data=invalid_data, format="json", HTTP_AUTHORIZATION=f"Basic {credentials}"
            )
            view = TaskRetrieveUpdateDestroyAPIView.as_view()
            response = view(req)
            response.render()
            modeladmin.message_user(request, "Task Saved Successfully", level="SUCCESS")

    save_task.short_description = "Save Task"

    def get_all_tasks(modeladmin, request, queryset):
        for task in queryset:
            url = reverse("task-retrieve", kwargs={"pk": 254})
            username = "lk"
            password = "livingstone"
            client = Client(
                HTTP_AUTHORIZATION=f"Basic {base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')}"
            )
            response = client.get(url)
            print(response.data)
            response.render()
            modeladmin.message_user(request, "All Tasks", level="SUCCESS")

    get_all_tasks.short_description = "Get all Tasks"

    def get_task(modeladmin, request, queryset):
        for task in queryset:
            url = reverse("task-retrieve", kwargs={"pk": task.id})
            username = "lk"
            password = "livingstone"
            client = Client(
                HTTP_AUTHORIZATION=f"Basic {base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')}"
            )
            response = client.get(url)
            response.render()
            modeladmin.message_user(request, "Task with PK", level="SUCCESS")

    get_task.short_description = "Get Task"

    def get_task_invalid(modeladmin, request, queryset):
        for task in queryset:
            url = reverse("task-retrieve", kwargs={"pk": 10000000000000000})
            username = "lk"
            password = "livingstone"
            client = Client(
                HTTP_AUTHORIZATION=f"Basic {base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')}"
            )
            response = client.get(url)
            response.render()
            modeladmin.message_user(request, "Task with Invalid PK", level="Error")

    get_task_invalid.short_description = "Get Task Invalid"

    def post_task(modeladmin, request, queryset):
        for task in queryset:
            factory = APIRequestFactory()
            url = reverse("tasks-list-create")
            data = {
                "title": "Test_Task",
                "description": "description",
                "due_date": "2024-12-01",
                "tags": ["Test_Tag", "Test_Tag"],
                "status": "OPEN",
            }
            username = "lk"
            password = "livingstone"
            credentials = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")
            req = factory.post(url, data=data, format="json", HTTP_AUTHORIZATION=f"Basic {credentials}")
            view = TaskRetrieveUpdateDestroyAPIView.as_view()
            response = view(req)
            response.render()
            modeladmin.message_user(request, "Task Created", level="SUCCESS")

    post_task.short_description = "Post Task"

    def post_task_illegal(modeladmin, request, queryset):
        for task in queryset:
            factory = APIRequestFactory()
            url = reverse("tasks-list-create")
            invalid_data = {
                "title": "Test_Task",
                "description": "description",
                "due_date": "2024-12-01",
                "test": "test",
            }
            username = "lk"
            password = "livingstone"
            credentials = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")
            req = factory.post(
                url, data=invalid_data, format="json", HTTP_AUTHORIZATION=f"Basic {credentials}"
            )
            view = TaskRetrieveUpdateDestroyAPIView.as_view()
            response = view(req)
            response.render()
            modeladmin.message_user(request, "Task Not Created", level="ERROR")

    post_task_illegal.short_description = "Post Task Illegal"

    def update_task_valid(modeladmin, request, queryset):
        for task in queryset:
            url = reverse("task-retrieve", kwargs={"pk": task.id})
            data = {"title": "Test_Task_Updated"}
            username = "lk"
            password = "livingstone"
            client = Client(
                HTTP_AUTHORIZATION=f"Basic {base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')}"
            )
            response = client.put(url, data=json.dumps(data), content_type="application/json")
            response.render()
            modeladmin.message_user(request, "Task Updated", level="SUCCESS")

    update_task_valid.short_description = "Update Task Valid"

    def update_task_invalid(modeladmin, request, queryset):
        for task in queryset:
            url = reverse("task-retrieve", kwargs={"pk": 10000000000000000})
            data = {"title": "Test_Task_Updated"}
            username = "lk"
            password = "livingstone"
            client = Client(
                HTTP_AUTHORIZATION=f"Basic {base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')}"
            )
            response = client.put(url, data=json.dumps(data), content_type="application/json")
            response.render()
            modeladmin.message_user(request, "Task with Invalid PK", level="ERROR")

    update_task_invalid.short_description = "Update Task Invalid"

    def update_task_illegal(modeladmin, request, queryset):
        for task in queryset:
            url = reverse("task-retrieve", kwargs={"pk": task.id})
            data = {"title": "Test_Task_Updated", "test": "test"}
            username = "lk"
            password = "livingstone"
            client = Client(
                HTTP_AUTHORIZATION=f"Basic {base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')}"
            )
            response = client.put(url, data=json.dumps(data), content_type="application/json")
            response.render()
            modeladmin.message_user(request, "Task with Illegal Items", level="ERROR")

    update_task_illegal.short_description = "Put Task Illegal"

    def update_task_due_date(modeladmin, request, queryset):
        for task in queryset:
            factory = APIRequestFactory()
            url = reverse("task-retrieve", kwargs={"pk": task.id})
            invalid_data = {"title": "Test_Task_Updated", "due_date": "2020-12-12"}
            username = "lk"
            password = "livingstone"
            credentials = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")
            req = factory.put(
                url, data=invalid_data, format="json", HTTP_AUTHORIZATION=f"Basic {credentials}"
            )
            view = TaskRetrieveUpdateDestroyAPIView.as_view()
            try:
                view(req)
            except Exception:
                modeladmin.message_user(request, "Task with Illegal Due Date", level="ERROR")

    update_task_due_date.short_description = "Put Task Due Date"

    def delete_task_valid(modeladmin, request, queryset):
        for task in queryset:
            url = reverse("task-retrieve", kwargs={"pk": task.id})
            username = "lk"
            password = "livingstone"
            client = Client(
                HTTP_AUTHORIZATION=f"Basic {base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')}"
            )
            response = client.delete(url)
            response.render()
            modeladmin.message_user(request, "Task Deleted", level="SUCCESS")

    delete_task_valid.short_description = "Delete Task Valid"

    def delete_task_invalid(modeladmin, request, queryset):
        for task in queryset:
            url = reverse("task-retrieve", kwargs={"pk": 10000000000000000})
            username = "lk"
            password = "livingstone"
            client = Client(
                HTTP_AUTHORIZATION=f"Basic {base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')}"
            )
            response = client.delete(url)
            response.render()
            modeladmin.message_user(request, "Task with Invalid PK", level="ERROR")

    delete_task_invalid.short_description = "Delete Task Invalid"

    actions = [
        update_task,
        save_task,
        get_all_tasks,
        get_task,
        get_task_invalid,
        post_task,
        post_task_illegal,
        update_task_valid,
        update_task_invalid,
        update_task_illegal,
        update_task_due_date,
        delete_task_valid,
        delete_task_invalid,
    ]


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "id")

    def test_get_tags(modeladmin, request, queryset):
        for tag in queryset:
            url = reverse("tag-list-create")
            username = "lk"
            password = "livingstone"
            client = Client(
                HTTP_AUTHORIZATION=f"Basic {base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')}"
            )
            response = client.get(url)
            response.render()
            modeladmin.message_user(request, "All Tags", level="SUCCESS")

    test_get_tags.short_description = "Get Tags"

    def post_tag(modeladmin, request, queryset):
        for tag in queryset:
            factory = APIRequestFactory()
            url = reverse("tag-list-create")
            data = {"name": "Test_Tag"}
            username = "lk"
            password = "livingstone"
            credentials = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")
            req = factory.post(url, data=data, format="json", HTTP_AUTHORIZATION=f"Basic {credentials}")
            view = TagListCreateAPIView.as_view()
            response = view(req)
            response.render()
            modeladmin.message_user(request, "Tag Created", level="SUCCESS")

    post_tag.short_description = "Post Tag"

    def post_tag_invalid(modeladmin, request, queryset):
        for task in queryset:
            factory = APIRequestFactory()
            url = reverse("tag-list-create")
            data = {"names": 1.0}
            username = "lk"
            password = "livingstone"
            credentials = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")
            req = factory.post(url, data=data, format="json", HTTP_AUTHORIZATION=f"Basic {credentials}")
            view = TagListCreateAPIView.as_view()
            response = view(req)
            response.render()
            modeladmin.message_user(request, "Tag Not Created", level="ERROR")

    post_tag_invalid.short_description = "Post Tag Invalid"

    def get_tag(modeladmin, request, queryset):
        for tag in queryset:
            url = reverse("tag-retrieve-update-destroy", kwargs={"pk": tag.id})
            username = "lk"
            password = "livingstone"
            client = Client(
                HTTP_AUTHORIZATION=f"Basic {base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')}"
            )
            response = client.get(url)
            response.render()
            modeladmin.message_user(request, "Tag with PK", level="SUCCESS")

    get_tag.short_description = "Get Tag"

    def get_tag_invalid(modeladmin, request, queryset):
        for tag in queryset:
            url = reverse("tag-retrieve-update-destroy", kwargs={"pk": 10000000000000000})
            username = "lk"
            password = "livingstone"
            client = Client(
                HTTP_AUTHORIZATION=f"Basic {base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')}"
            )
            response = client.get(url)
            response.render()
            modeladmin.message_user(request, "Tag with Invalid PK", level="Error")

    get_tag_invalid.short_description = "Get Tag Invalid"

    def put_tag_valid(modeladmin, request, queryset):
        for tag in queryset:
            url = reverse("tag-retrieve-update-destroy", kwargs={"pk": tag.id})
            data = {"name": "Test_Tag_Updated"}
            username = "lk"
            password = "livingstone"
            client = Client(
                HTTP_AUTHORIZATION=f"Basic {base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')}"
            )
            response = client.put(url, data=json.dumps(data), content_type="application/json")
            response.render()
            modeladmin.message_user(request, "Tag Updated", level="SUCCESS")

    put_tag_valid.short_description = "Update Tag Valid"

    def put_tag_invalid(modeladmin, request, queryset):
        for tag in queryset:
            url = reverse("tag-retrieve-update-destroy", kwargs={"pk": tag.id})
            data = {"names": "Test_Tag_Updated"}
            username = "lk"
            password = "livingstone"
            client = Client(
                HTTP_AUTHORIZATION=f"Basic {base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')}"
            )
            response = client.put(url, data=json.dumps(data), content_type="application/json")
            response.render()
            modeladmin.message_user(request, "Tag Not Updated", level="ERROR")

    put_tag_invalid.short_description = "Update Tag Invalid"

    def put_tag_invalid_id(modeladmin, request, queryset):
        for tag in queryset:
            url = reverse("tag-retrieve-update-destroy", kwargs={"pk": 10000000000000000})
            data = {"name": "Test_Tag_Updated"}
            username = "lk"
            password = "livingstone"
            client = Client(
                HTTP_AUTHORIZATION=f"Basic {base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')}"
            )
            response = client.put(url, data=json.dumps(data), content_type="application/json")
            response.render()
            modeladmin.message_user(request, "Tag with Invalid PK", level="Error")

    put_tag_invalid_id.short_description = "Put Tag Invalid PK"

    def delete_tag_valid(modeladmin, request, queryset):
        for tag in queryset:
            url = reverse("tag-retrieve-update-destroy", kwargs={"pk": tag.id})
            username = "lk"
            password = "livingstone"
            client = Client(
                HTTP_AUTHORIZATION=f"Basic {base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')}"
            )
            response = client.delete(url)
            response.render()
            modeladmin.message_user(request, "Tag Deleted", level="SUCCESS")

    delete_tag_valid.short_description = "Delete Tag Valid"

    def delete_tag_invalid(modeladmin, request, queryset):
        for task in queryset:
            url = reverse("tag-retrieve-update-destroy", kwargs={"pk": 10000000000000000})
            username = "lk"
            password = "livingstone"
            client = Client(
                HTTP_AUTHORIZATION=f"Basic {base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')}"
            )
            response = client.delete(url)
            response.render()
            modeladmin.message_user(request, "Tag with Invalid PK", level="ERROR")

    delete_tag_invalid.short_description = "Delete Tag Invalid"

    actions = [
        test_get_tags,
        post_tag,
        post_tag_invalid,
        get_tag,
        get_tag_invalid,
        put_tag_valid,
        put_tag_invalid,
        put_tag_invalid_id,
        delete_tag_valid,
        delete_tag_invalid,
    ]


admin.site.register(Task, TaskAdmin)
admin.site.register(Tag, TagAdmin)
