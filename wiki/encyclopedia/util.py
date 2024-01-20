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
        if not check_file(entry_name):
            markdown_text = get_entry(entry_name)
            find_page(entry_name, markdown_text)
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

#function to write the html code after conversion to a new html file
def write_html(title, html_text):
    with open(f"encyclopedia/templates/encyclopedia/{title}.html", 'a')as f:
        f.write(formatted_string("extends", "\"encyclopedia/layout.html\""))
        f.write(formatted_string("block", "title"))
        f.write(f"\t{title}\n")
        f.write(formatted_string("endblock"))
        f.write(formatted_string("block", "body"))
        f.write(f"{html_text}\n")
        f.write(formatted_string("endblock"))
        
#function to check whther a file exist or not
def check_file(title):
    return os.path.isfile(f"encyclopedia/templates/encyclopedia/{title}.html")

#function to return a string that to append into the html file
def formatted_string(name, text=None):
    if text != None:
        return "{% "+ name + " " + text + " %}\n"
    return "{% "+ name + " %}\n"

#function to find a page 
def find_page(title, markdown_text):
    if not check_file(title):
        html_text = markdown2.markdown(markdown_text)
        write_html(title, html_text)

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