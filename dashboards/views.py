from django.shortcuts import render,redirect,get_object_or_404
from blogs.models import Category,Blog
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm,BlogPostForm
from blogs.models import Blog
from django.template.defaultfilters import slugify
# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    category_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()
    context = {
        'category_count':category_count,
        'blogs_count':blogs_count,
    }
    return render(request,'dashboard/dashboard.html',context)

def categories(request):
    return render(request,'dashboard/categories.html')

# views for the CRUD opetaion of category.
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm()
    context = {
        'form':form,
    }
    return render(request,'dashboard/add_category.html',context)

def edit_category(request,pk):
    # With this instance we are giving the already filled value to edit.
    category = get_object_or_404(Category,pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category )  # with request.POST we are taking the value that we are want to update. instance=category this is existing value.
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm(instance=category)
    context = {
        'form':form,
        'category':category,
    }
    return render(request,'dashboard/edit_category.html',context)

def delete_category(request,pk):
    category = get_object_or_404(Category,pk=pk)
    category.delete()
    return redirect('categories')

# View for CRUD opetaion of posts.
def posts(request):
    posts = Blog.objects.all()
    context = {
        'posts':posts,
    }
    return render(request,'dashboard/posts.html',context)

def add_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST,request.FILES) # Whenever you upload any kind of file image , pdf try to use this.
        if form.is_valid():
            # Below is the way to assign the mandatory field.
            post = form.save(commit=False) # temporary saving the form because in our Blog model author is mandatory field but we are not providing it.
            post.author = request.user
            print("Before save:", post.pk)
            post.save()
            # Here we are getting title.
            print("After save:", post.pk)
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id) # we should add the pk to make the slug unique.
            print("Generated slug:", post.slug)
            post.save()
            return redirect('posts')
        else:
            print(form.errors)
    form = BlogPostForm()
    context={
        'form':form,
    }
    return render(request,'dashboard/add_post.html',context)


def edit_post(request,pk):
    post = get_object_or_404(Blog,pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES,instance = post)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title)+ '-' + str(post.id)
            post.save()
            return redirect('posts')
    form = BlogPostForm(instance=post)
    context = {
        'form':form,
        'post':post,
    }
    return render(request,'dashboard/edit_post.html',context)

def delete_post(request,pk):
    post = get_object_or_404(Blog,pk=pk)
    post.delete()
    return redirect('posts')

