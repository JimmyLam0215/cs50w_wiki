import random
import re
import os.path
import markdown2
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    entry_names = []
    for filename in filenames:
        if filename.endswith(".md"):
            entry_name = re.sub(r"\.md$", "", filename)
            entry_names.append(entry_name)
    return list(sorted(entry_names))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))

def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
        
#function to check whether a md file exist or not
def check_file(title):
    return os.path.isfile(f"entries/{title}.md")

#function to return a string that to append into the html file
def formatted_string(name, text=None):
    if text != None:
        return "{% "+ name + " " + text + " %}\n"
    return "{% "+ name + " %}\n"

#function to find a page where the markdown language is converted to html
def find_page(title):
    markdown_text = get_entry(title)
    if markdown_text != None:
        markdowner = markdown2.Markdown()
        return markdowner.convert(markdown_text)
    return None
    
#function to return a list that stored all the name of the markdown file
def get_file_name():
    _, filenames = default_storage.listdir("entries")
    entry_names = []
    for filename in filenames:
        if filename.endswith(".md"):
            entry_name = re.sub(r"\.md$", "", filename)
            entry_names.append(entry_name)
    return entry_names

#function to randomly choose one webpage
def random_page():
    entry_names = get_file_name()
    random_num = random.randrange(0, len(entry_names))
    return entry_names[random_num]

#function to check whether the keyword exist in the entries folder
def check_page_name(name):
    page_names = list_entries()
    page_names_to_lower = [page_name.lower() for page_name in page_names]
    return name in page_names_to_lower

#function to return a list of names that fit the page name
def get_search_results(name):
    all_entries = list_entries()
    results = []
    for entry in all_entries:
        if name.lower() in entry.lower():
            results.append(entry)
    return results

