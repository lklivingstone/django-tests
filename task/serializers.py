from rest_framework import serializers
from .models import Task, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class CustomTagField(serializers.RelatedField):
    def get_queryset(self):
        return Tag.objects.all()

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        try:
            tag = Tag.objects.get(name=data)
        except Tag.DoesNotExist:
            tag = Tag.objects.create(name=data)
        return tag


class TaskSerializer(serializers.ModelSerializer):
    tags = CustomTagField(many=True)

    class Meta:
        model = Task
        fields = "__all__"

    def create(self, validated_data):
        tags_data = validated_data.pop("tags")

        # Create a new Task instance with the extracted data
        task = Task.objects.create(**validated_data)

        for tag_data in tags_data:
            task.tags.add(tag_data)
        return task

    def update(self, instance, validated_data):
        # Update the individual fields of the instance
        instance.title = validated_data.pop("title", instance.title)
        instance.description = validated_data.pop("description", instance.description)
        instance.due_date = validated_data.pop("due_date", instance.due_date)
        instance.status = validated_data.pop("status", instance.status)

        # Remove all existing tags from the task
        if "tags" in validated_data:
            tags_data = validated_data.pop("tags")
            instance.tags.clear()
            for tag_data in tags_data:
                instance.tags.add(tag_data)

        instance.save()
        return instance
