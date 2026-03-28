from django.shortcuts import render, redirect, get_object_or_404
from .models import Proposal
from .forms import ProposalForm
from core.models import Task

def submit_proposal(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        form = ProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.task = task
            proposal.save()
            return redirect('tasks:task_detail', pk=task.id)
    else:
        form = ProposalForm()
    
    return render(request, 'proposals/submit_proposal.html', {
        'form': form,
        'task': task
    })

def task_proposals(request, task_id):
    """Optional: View all proposals for a task (for demo)"""
    task = get_object_or_404(Task, id=task_id)
    proposals = task.proposals.all()
    return render(request, 'proposals/task_proposals.html', {
        'task': task,
        'proposals': proposals
    })