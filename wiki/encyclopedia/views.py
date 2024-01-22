from django.shortcuts import redirect, render

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_entry(request, title):
    markdown_text = util.get_entry(title)
    if markdown_text != None:
        util.find_page(title, markdown_text)
        return render(request, f"encyclopedia/{title}.html")
    else:
        return render(request, "encyclopedia/missing.html")
        
def create(request):
    if request.method == "POST":
        title = request.POST.get("title", "")
        content = request.POST.get("description", "")
        content = f"# {title}\n"+ content
        if(not util.check_file(title) and title != None and content != None):
            util.save_entry(title, content)
            markdown_text = util.get_entry(title)
            util.find_page(title, markdown_text)
            return render(request, f"encyclopedia/{title}.html")
        else:
            return render(request, "encyclopedia/create_failed.html")
    return render(request, "encyclopedia/create.html")
        
def random(request):
    random_page = util.random_page()
    return render(request, f"encyclopedia/{random_page}.html")

def search(request):
    query = request.GET.get('q', '')
    if util.check_page_name(query.lower()):
        return render(request, f"encyclopedia/{query}.html")
    else:
        util.get_search_results(query)
        return render(request, "encyclopedia/search.html", {
            "entries": util.get_search_results(query)
        })
           
def edit(request):
    return render(request, "encyclopedia/edit.html")
    