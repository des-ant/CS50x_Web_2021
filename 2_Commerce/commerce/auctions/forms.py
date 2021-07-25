from django.forms import ModelForm
from .models import Category, Listing


class NewListingForm(ModelForm):
    """
    New listing form from listing model
    """
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'image', 'category']