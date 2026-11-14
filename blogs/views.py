from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Blog,Category
from django.db.models import Q
# Create your views here.
def post_by_category(request,category_id):
    # Fetch the post that belong to category with the category_id
    posts = Blog.objects.filter(status= 'Published',category_id=category_id)
    #Use try and except when we want to do some custom action if category does not exist.
    try:
        category = Category.objects.get(pk=category_id)
    except:
        # redirect the user to home page.
        return redirect('home')
    # Use get_object_or_404 if we want to show the 404 error page.
    context = {
        'posts':posts,
        'category':category,
    }
    return render(request,'post_by_category.html',context)

def blogs(request,slug):
    single_blog = get_object_or_404(Blog,slug=slug, status='Published')
    context = {
        'single_blog':single_blog,
    }
    return render(request, 'blogs.html',context)

def search(request):
    keyword = request.GET.get('keyword')
    blogs = Blog.objects.filter(Q(title__icontains=keyword)| Q(short_description__icontains=keyword)|Q(blog_body__icontains=keyword),status='Published')
    context = {
        'blogs':blogs,
        'keyword':keyword,
    }
    return render(request,'search.html',context)