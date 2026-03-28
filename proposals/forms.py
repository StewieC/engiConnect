from django import forms
from .models import Proposal

class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['bidder_name', 'bidder_email', 'proposed_price', 'delivery_days', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 5}),
            'proposed_price': forms.NumberInput(attrs={'step': '100'}),
        }