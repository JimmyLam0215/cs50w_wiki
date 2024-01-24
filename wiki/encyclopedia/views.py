from django.shortcuts import redirect, render

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_entry(request, title):
    content = util.find_page(title)
    if content != None:
        return render(request, f"encyclopedia/entry.html", {
            "name": title,
            "content": content,
            "state": "normal"
        })
    else:
        return render(request, "encyclopedia/missing.html")
        
def create(request):
    if request.method == "POST":
        title = request.POST.get("title", "")
        content = request.POST.get("description", "")
        content = f"# {title}\n"+ content
        if(not util.check_file(title) and title != None and content != None):
            util.save_entry(title, content)
            markdown_content = util.find_page(title)
            return render(request, f"encyclopedia/entry.html", {
                "name": title,
                "content": markdown_content,
                "state": "normal"
            })
        else:
            return render(request, "encyclopedia/create_failed.html")
    return render(request, "encyclopedia/create.html")
        
def random(request):
    random_page = util.random_page()
    content = util.find_page(random_page)
    return render(request, f"encyclopedia/entry.html", {
        "name": random_page,
        "content": content,
        "state": "normal"
    })

def search(request):
    query = request.GET.get('q', '')
    if util.check_page_name(query.lower()):
        content = util.find_page(query)
        return render(request, f"encyclopedia/entry.html", {
            "name": query,
            "content": content,
            "state": "normal"
        })
    else:
        util.get_search_results(query)
        return render(request, "encyclopedia/search.html", {
            "entries": util.get_search_results(query)
        })
           
def edit(request):
    if request.method == "POST":
        title = request.POST.get("entry_title", "")
        file_content = util.get_entry(title)
        return render(request, "encyclopedia/edit_save.html", {
            "title": title,
            "content": file_content,
        })

def edit_save(request):
    if request.method == "POST":
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        util.save_entry(title, description)
        content = util.find_page(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })

    