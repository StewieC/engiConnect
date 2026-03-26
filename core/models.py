from django.db import models
from django.utils import timezone

class Task(models.Model):
    CATEGORY_CHOICES = [
        ('mechanical', 'Mechanical Design / CAD'),
        ('electrical', 'Electrical / Electronics'),
        ('civil', 'Civil / Structural'),
        ('software', 'Software / Programming'),
        ('chemical', 'Chemical / Process Engineering'),
        ('other', 'Other Engineering'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open - Bids Welcome'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    budget = models.DecimalField(max_digits=10, decimal_places=2, help_text="Expected budget in KES")
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    attachments_note = models.TextField(blank=True, null=True, 
                                      help_text="Describe any files you plan to attach")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Engineering Task"
        verbose_name_plural = "Engineering Tasks"