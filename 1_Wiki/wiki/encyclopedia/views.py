from random import choice
from markdown2 import Markdown
from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Function to render encyclopedia entries to html page
def wiki(request, title):
    # Read markdown file
    md_file = util.get_entry(title)
    if md_file is None:
        # Return error page with requested title
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    # Convert markdown to html and send data to template
    return render(request, "encyclopedia/entry.html", {
        "entry": Markdown().convert(md_file)
    })

# Function to take user to random encyclopedia entry
def random_entry(request):
    # Get random encyclopedia entry
    random_entry = choice(util.list_entries())
    return wiki(request, random_entry)

# Django form, inherits from forms.form
class new_entry_form(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

# Function to create new entry
def new_entry(request):
    # If new entry being submitted
    if request.method == "POST":
        form = new_entry_form(request.POST)
        # Check for valid input
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # Add markdown title to content
            content = f"# {title}\n{content}"
            # If entry exists, present error message
            if util.get_entry(title):
                messages.error(request, "Error: Page already exists")
                # Send back existing form data
                return render(request, "encyclopedia/newentry.html", {
                    "form": form
                })
            # Save entry to disk and take user to new entry's page
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:wiki", args=[title]))
        # Invalid input, send back existing form data
        else:
            return render(request, "encyclopedia/newentry.html", {
                "form": form
            })
    # Render empty form if received get request
    return render(request, "encyclopedia/newentry.html", {
        "form": new_entry_form()
    })