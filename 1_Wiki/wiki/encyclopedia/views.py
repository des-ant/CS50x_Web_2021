from markdown2 import Markdown
from django.http import HttpResponse
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

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