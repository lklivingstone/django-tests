from django.urls import path
from .views import (
    TaskRetrieveUpdateDestroyAPIView,
    TagListCreateAPIView,
    TagRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    # Endpoint for listing and creating tasks
    path("tasks/", TaskRetrieveUpdateDestroyAPIView.as_view(), name="tasks-list-create"),
    # Endpoint for retrieving, updating, and deleting a specific task
    path(
        "tasks/<int:pk>/",
        TaskRetrieveUpdateDestroyAPIView.as_view(),
        name="task-retrieve",
    ),
    # Endpoint for listing and creating tags
    path("tags/", TagListCreateAPIView.as_view(), name="tag-list-create"),
    # Endpoint for retrieving, updating, and deleting a specific tag
    path(
        "tags/<int:pk>/",
        TagRetrieveUpdateDestroyAPIView.as_view(),
        name="tag-retrieve-update-destroy",
    ),
]
