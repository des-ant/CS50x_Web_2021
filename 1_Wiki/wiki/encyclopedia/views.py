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


def wiki(request, title):
    """
    Renders encyclopedia entries to html page
    """
    # Read markdown file
    md_file = util.get_entry(title)
    if md_file is None:
        # Return error page with requested title
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    # Convert markdown to html and send data to template
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": Markdown().convert(md_file)
    })


def random_entry(request):
    """
    Renders random encyclopedia entry
    """
    # Get random encyclopedia entry
    random_entry = choice(util.list_entries())
    return wiki(request, random_entry)


class new_entry_form(forms.Form):
    """
    Django new entry form, inherits from forms.Form
    """
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}), label="Content")


def new_entry(request):
    """
    Create new encyclopedia entry
    """
    # If new entry being submitted
    if request.method == "POST":
        form = new_entry_form(request.POST)
        # Check for valid input
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # Add markdown title to content, add newline before and after content
            content = f"# {title}\n\n{content}\n"
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


class edit_entry_form(forms.Form):
    """
    Django edit entry form, inherits from forms.Form
    """
    content = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}), label="Content")


def edit_entry(request, title):
    """
    Edit encyclopedia entry
    """
    # Read markdown file
    md_file = util.get_entry(title)
    if md_file is None:
        # Return error page with requested title
        return render(request, "encyclopedia/error.html", {
            "title": title
        })

    # Split markdown file into title and content
    md_partition = md_file.partition('\n')
    # Get first line from markdown file
    first_line = md_partition[0]
    # Remove first two characters (markdown heading)
    heading = first_line[2:]
    # Content is in partition after newline
    content_section = md_partition[2]
    # Get page content from markdown file by removing first and last lines
    content = '\n'.join(content_section.split('\n')[1:-1])

    # If edited entry being submitted
    if request.method == "POST":
        form = edit_entry_form(request.POST)
        # Check for valid input
        if form.is_valid():
            content = form.cleaned_data["content"]
            # Add markdown title to content, add newline before and after content
            content = f"# {heading}\n\n{content}\n"
            # Save entry to disk and take user to new entry's page
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:wiki", args=[title]))
        # Invalid input, send back existing form data
        else:
            return render(request, "encyclopedia/editentry.html", {
                "title": title,
                "heading": heading,
                "form": form 
            })
    # Populate form with encyclopedia entry content
    return render(request, "encyclopedia/editentry.html", {
        "title": title,
        "heading": heading,
        "form": edit_entry_form(initial={"content": content})
    })
