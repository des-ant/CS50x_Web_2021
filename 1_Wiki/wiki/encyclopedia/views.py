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
    # # Get first line from markdown file
    # first_line = css_md.partition('\n')[0]
    # # Remove first two characters (markdown heading)
    # heading = first_line[2:]
    # print(heading)
    if md_file is None:
        return HttpResponse("Requested page not found")
    return HttpResponse(md_file)