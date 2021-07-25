from django import forms
from .models import Category, Listing


class NewCategoryForm(forms.ModelForm):
    """
    New category form from category model
    """
    class Meta:
        model = Category
        fields = ['name']
        # Add classes for bootstrap styling
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"})
        }
        labels = {
            'name': "Create New Category"
        }


class NewListingForm(forms.ModelForm):
    """
    New listing form from listing model
    """
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'image', 'category']
        # Add classes for bootstrap styling
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={"class": "form-control"}),
            'price': forms.NumberInput(attrs={"class": "form-control"}),
            'image': forms.FileInput(attrs={"class": "form-control"}),
            'category': forms.Select(attrs={"class": "form-control"})
        }