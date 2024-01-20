from django.shortcuts import render

from . import util
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_entry(request, title):
    markdown_text = util.get_entry(title)
    if markdown_text != None:
        html_text = markdown2.markdown(markdown_text)
        util.write_html(title, html_text)
        return render(request, f"encyclopedia/{title}.html")
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
        
