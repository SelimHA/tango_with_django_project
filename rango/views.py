from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect
from rango.forms import PageForm
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.

def about(request):
        return render(request, 'rango/about.html', {})
def index(request):
        # Make query, order database by likes (desc) and only show top 5
        category_list = Category.objects.order_by('-likes')[:5]
        pages_list = Page.objects.order_by('-views')[:5]
        context_dict = {}
        context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
        context_dict['categories'] = category_list
        context_dict['pages'] = pages_list
        # Render response
        return render(request, 'rango/index.html', context=context_dict)
def show_category(request, category_name_slug):
        context_dict = {}
        try:
                # Get model of category or raise exception if doesnt exist
                category = Category.objects.get(slug=category_name_slug)
                # Get all associated pages in list
                pages = Page.objects.filter(category=category)
                context_dict['pages'] = pages
                context_dict['category'] = category
        except Category.DoesNotExist:
                # Category doesnt exist so dont do anything
                context_dict['category'] = None
                context_dict['pages'] = None
        # Go render the response and return it to the client.
        return render(request, 'rango/category.html', context=context_dict)


def add_category(request):
        form = CategoryForm()
        # A HTTP POST?
        if request.method == 'POST':
                form = CategoryForm(request.POST)
                # Have we been provided with a valid form?
                if form.is_valid():
                        # Save the new category to the database.
                        form.save(commit=True)
                        # Now that the category is saved, we could confirm this.
                        # For now, just redirect the user back to the index view.
                        return redirect(reverse('rango:index'))
                else:
                        # The supplied form contained errors -
                        # just print them to the terminal.
                        print(form.errors)
        # Will handle the bad form, new form, or no form supplied cases.
        # Render the form with error messages (if any).
        return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None
    
    # You cannot add a page to a Category that does not exist... DM
    if category is None:
        return redirect(reverse('rango:index'))

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)  # This could be better done; for the purposes of TwD, this is fine. DM.
    
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)
