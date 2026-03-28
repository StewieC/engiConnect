from django.urls import path
from . import views

app_name = 'proposals'

urlpatterns = [
    path('task/<int:task_id>/proposal/', views.submit_proposal, name='submit_proposal'),
    path('task/<int:task_id>/proposals/', views.task_proposals, name='task_proposals'),
]