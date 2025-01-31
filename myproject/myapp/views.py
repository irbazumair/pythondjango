from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, PostForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Post


def home(request):
    name = 'Umair'
    nums = {1,2,3,4,5,6,7,8,9,10}
    context = {'name':name, 'nums':nums }   
    
    return render(request,'home.html', context)


def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            error = 'invalid username or password'
            context = {'error': error}
            return render(request, 'login.html', context)

def register(request):
    form = UserRegistrationForm()
    context = {'form': form}
    if request.method == 'GET':
        return render(request, 'register.html', context)

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            context['error']= 'Invalid form submission,try again'
            return render(request, 'register.html', context)
        
        
def user_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def create_post(request):
    form = PostForm()
    context = {'form': form}
    
    if request.method == 'GET':
        return render(request, 'create-post.html', context)
    
    if request.method == 'POST':
        form = PostForm(request.POST)


    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user 
        post.save()
        return redirect('home')
    else:
        context['error'] = 'Invalid form submission,try again'
        return render(request, 'create-post.html', context)
        
        
def view_posts(request):
    post_list = Post.objects.all()
    
    context = {'post_list': post_list}
    return render(request, 'view-post.html', context)

def update_post (request, id):
    post = Post.objects.get(pk=id) #returns single post
    
    form = PostForm(instance=post)
    
    context = {'form': form}
    if request.method == 'GET':
        return render(request, 'update-post.html', context)

    if request.method =='POST':
        form = PostForm(request.POST, instance=post)
        
        if form.is_valid():
            form.save()
            return redirect('view-post')
    