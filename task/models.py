from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


# Model for Tag
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Model for Task
class Task(models.Model):
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("WORKING", "Working"),
        ("DONE", "Done"),
        ("OVERDUE", "Overdue"),
    ]

    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=1000, blank=False, null=False)
    due_date = models.DateField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="OPEN", blank=False, null=False)

    def __str__(self):
        return self.title

    # Custom validation: Check if due date is before current timestamp
    def clean(self):
        current_timestamp = timezone.now()
        if self.due_date and self.due_date < current_timestamp.date():
            raise ValidationError("Due Date cannot be before Timestamp created.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        # Remove duplicate tags
        self.tags.set(list(set(self.tags.all())))
