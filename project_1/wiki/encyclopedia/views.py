from logging import PlaceHolder
from django.shortcuts import render
from . import util
import markdown2
from django import forms
import re
import random


class Search(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class EntryTitle(forms.Form):
    entry_title = forms.CharField(label="Entry Titel", widget=forms.TextInput(attrs={'placeholder': 'Write Title'}))
    entry_content = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Write Content'}))

class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(), label='')


def random_page(request):
    name_of_page = random.choice(util.list_entries())
    content_of_title = util.get_entry(name_of_page)
    converted_content_of_title = markdown2.markdown(content_of_title)
    return render(request, "encyclopedia/title.html", {
            "title_up": name_of_page,
            "converted_content_of_title": converted_content_of_title,
            "form": Search()
        })

def edit(request, title):
    if request.method == 'POST':
        form = Edit(request.POST) 
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title,textarea)
            content = util.get_entry(title)
            content_converted = markdown2.markdown(content)
            return render(request, "encyclopedia/title.html", {
                'form': Search(),
                'converted_content_of_title': content_converted,
                'title_up': title
            })

    else: #GET
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            'content_to_edit': Edit(initial={'textarea': content}),
            'title_up': title,
            'form': Search(),
        })


def new_entry(request):
    if request.method == "POST":
        entry_title_post = EntryTitle(request.POST)
        #entry_content_post = EntryContent(request.POST)
        if entry_title_post.is_valid():
            title_saved = entry_title_post.cleaned_data["entry_title"]
            content_saved = entry_title_post.cleaned_data["entry_content"]
            all_entries = util.list_entries()
            for search in all_entries:
                if title_saved.lower() == search.lower():
                    return render(request, "encyclopedia/new_entry.html", {
                    "entry_title_get": EntryTitle(),
                    "error_message": "This Entry already exist",
                    "form": Search()
                    })
            util.save_entry(title_saved, content_saved)
            #return title(request, title_saved) # not sure if this is allowed
            #  Why title is not seen in URL????
            content_of_title = util.get_entry(title_saved)
            converted_content_of_title = markdown2.markdown(content_of_title)
            return render(request, "encyclopedia/title.html", {
                    "title_up": title_saved,
                    "converted_content_of_title": converted_content_of_title,
                    "form": Search()
                })
            #return HttpResponseRedirect('/wiki/<str:title_saved>')
        else:
            return render(request, "encyclopedia/new_entry.html", {
                "entry_title_get": EntryTitle(),
                #"entry_content_get": EntryContent(),
                "form": Search()
            })  
    else: #GET
        return render(request, "encyclopedia/new_entry.html", {
                    "entry_title_get": EntryTitle(),
                    #"entry_content_get": EntryContent(),
                    "form": Search()
                })

def index(request):
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            title_searched = form.cleaned_data["title"]
            all_entries = util.list_entries()
            substring_list = []
            for search in all_entries:
                if search.lower() == title_searched.lower():
                    #return title(request, search) # not sure if this is allowed
                    #  Why title is not seen in URL????
                    content_of_title = util.get_entry(search)
                    converted_content_of_title = markdown2.markdown(content_of_title)
                    return render(request, "encyclopedia/title.html", {
                            "title_up": search,
                            "converted_content_of_title": converted_content_of_title,
                            "form": Search()
                        })
                elif re.findall(title_searched.lower(), search.lower()):
                    substring_list.append(search)
            if len(substring_list) >= 1:
                return render(request, "encyclopedia/search.html", {
                        "entries": substring_list,
                        # How to avoid redundancy with the NetTaskForm() which appears on various places??
                        "form": Search()
                        })
            else:
                return render(request, "encyclopedia/index.html", {
                "form": Search(),
                "no_results": "No results found."
                })
                   
        else:
            return render(request, "encyclopedia/index.html", {
                        "entries": util.list_entries(),
                        "form": Search()
                    })

    else: # GET
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": Search(),
        })
        

def title(request, title):
    if util.get_entry(title) is None:
            error_message = "Your requested page was not found. Try another."
            error_code = "404 Not Found"
            return render(request, "encyclopedia/error.html", {
                "error_message": error_message,
                "title_up": error_code,
                "form": Search()
            })
    else:
        content_of_title = util.get_entry(title)
        converted_content_of_title = markdown2.markdown(content_of_title)
        return render(request, "encyclopedia/title.html", {
                "title_up": title,
                "converted_content_of_title": converted_content_of_title,
                "form": Search()
            })