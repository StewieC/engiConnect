from django.db import models
from core.models import Task

class Proposal(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='proposals')
    
    # For now (demo mode) we'll just store a name/email. Later this will link to User
    bidder_name = models.CharField(max_length=150)
    bidder_email = models.EmailField()
    
    proposed_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_days = models.PositiveIntegerField(help_text="Number of days to complete the task")
    cover_letter = models.TextField(help_text="Why you are the best fit for this task")
    
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending Review'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )

    def __str__(self):
        return f"Proposal for '{self.task.title}' by {self.bidder_name}"

    class Meta:
        ordering = ['-created_at']