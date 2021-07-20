from .models import ProductReview
from django import forms

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ('content', 'product', 'reviewer', 'rating')
        widgets = {'product': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}