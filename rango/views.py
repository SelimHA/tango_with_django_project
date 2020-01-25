from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page

# Create your views here.

def about(request):
        context_dict = {'your_name': 'Selim Hadjadj-Aoul'}
        return render(request, 'rango/about.html', context=context_dict)
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
