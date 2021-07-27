from django import forms
from .models import Category, Listing, Bid


class NewCategoryForm(forms.ModelForm):
    """
    New category form from category model
    """
    class Meta:
        model = Category
        fields = ['name']
        # Add classes for bootstrap styling
        # Add list for datalist input
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control", "list": "categories"})
        }
        labels = {
            'name': "Category"
        }


class NewListingForm(forms.ModelForm):
    """
    New listing form from listing model
    """
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'image']
        # Add classes for bootstrap styling
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={"class": "form-control"}),
            'price': forms.NumberInput(attrs={"class": "form-control"}),
            'image': forms.FileInput(attrs={"class": "form-control"})
        }


class NewBidForm(forms.ModelForm):
    """
    New bid form from bid model
    """
    class Meta:
        model = Bid
        fields = ['price']
        # Add classes for bootstrap styling
        widgets = {
            'price': forms.NumberInput(attrs={"class": "form-control", "placeholder": "Bid"})
        }
        labels = {
            'price': "Enter bid here:"
        }