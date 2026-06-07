from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task, User_table
from django.contrib.auth.models import User, Group
from datetime import datetime


# ── LOGIN ──
def login_get(request):
    return render(request, 'user/loginindex.html')

def login_post(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/home_get/')
        else:
            messages.warning(request, 'Invalid username or password')
            return redirect('/login_get/')

# ── LOGOUT ──
def logout_get(request):
    logout(request)
    return render(request, 'user/loginindex.html')

# ── REGISTER ──
def register_get(request):
    return render(request, 'user/register.html')

def register_post(request):
    try:
        Name = request.POST['name']
        DOB = request.POST['dob']
        Gender = request.POST['gender']
        Photo = request.FILES['photo']

        fs = FileSystemStorage()
        path = fs.save(Photo.name, Photo)
        Place = request.POST['place']
        Post = request.POST['post']
        Pin = request.POST['pin']
        Phone = request.POST['phone']
        Email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create(username=username, password=make_password(password), first_name=Name, email=Email)
        user.save()
        user.groups.add(Group.objects.get(name='User'))

        a = User_table()
        a.LOGIN = user
        a.Name = Name
        a.DOB = DOB
        a.Gender = Gender
        a.Photo = path
        a.Place = Place
        a.Post = Post
        a.Pin = Pin
        a.Phone = Phone
        a.Email = Email
        a.save()
        messages.success(request, 'Registration successful! Please login.')
        return redirect('/login_get/#aaa')
    except IntegrityError:
        return render(request, 'user/register.html', {
            'error': 'Username or email already exists. Please try another.'
        })

# ── HOME ──
@login_required(login_url='/login_get/')
def home_get(request):
    return render(request, 'user/home.html')

# ── VIEW PROFILE ──
@login_required(login_url='/login_get/')
def view_profile(request):
    user_profile = User_table.objects.get(LOGIN=request.user)
    return render(request, 'user/view_profile.html', {'profile': user_profile})

# ── EDIT PROFILE ──
@login_required(login_url='/login_get/')
def edit_profile_get(request):
    user_profile = User_table.objects.get(LOGIN=request.user)
    return render(request, 'user/edit_profile.html', {'profile': user_profile})

@login_required(login_url='/login_get/')
def edit_profile_post(request):

    user_profile = User_table.objects.get(LOGIN=request.user)

    user_profile.Name = request.POST['name']
    user_profile.DOB = request.POST['dob']
    user_profile.Gender = request.POST['gender']
    user_profile.Place = request.POST['place']
    user_profile.Post = request.POST['post']
    user_profile.Pin = request.POST['pin']
    user_profile.Phone = request.POST['phone']
    user_profile.Email = request.POST['email']

    # Update photo only if a new one is selected
    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        filename = fs.save(photo.name, photo)
        user_profile.Photo = filename

    user_profile.save()

    # Update Django User table also
    request.user.first_name = request.POST['name']
    request.user.email = request.POST['email']
    request.user.save()

    messages.success(request, 'Profile Updated Successfully!')
    return redirect('/view_profile/')

# ── VIEW TASKS ──
@login_required(login_url='/login_get/')
def view_tasks_get(request):
    tasks = Task.objects.filter(User__LOGIN=request.user)
    return render(request, 'user/view_tasks.html', {'tasks': tasks})

@login_required(login_url='/login_get/')
def view_tasks_post(request):
    name=request.POST['search']
    ob=Task.objects.filter(Title__icontains=name, User__LOGIN=request.user)
    return render(request, "user/view_tasks.html",{"tasks":ob,'name':name})

# ── ADD TASK ──
@login_required(login_url='/login_get/')
def add_task_get(request):
    return render(request, 'user/add_task.html')

@login_required(login_url='/login_get/')
def add_task_post(request):
    Title       = request.POST['title']
    Description = request.POST['description']
    Priority    = request.POST['priority']
    d_date      = request.POST['due_date']

    a = Task()
    a.User         = User_table.objects.get(LOGIN__id=request.user.id)
    a.Title        = Title
    a.Description  = Description
    a.Priority     = Priority
    a.Created_date = datetime.now().date()
    a.Due_date     = d_date
    a.Status       = 'Pending'   # ← auto set since no form field
    a.save()

    messages.success(request, 'Task Added')
    return redirect('/view_tasks_get/#aaa')

# ── EDIT TASK ──
@login_required(login_url='/login_get/')
def edit_task_get(request, task_id):
    task = Task.objects.get(id=task_id)
    request.session['id'] = task_id    # ← save to session
    return render(request, 'user/edit_task.html', {'task': task})

@login_required(login_url='/login_get/')
def edit_task_post(request):           # ← no task_id parameter
    task = Task.objects.get(id=request.session['id'])  # ← get from session
    task.Title = request.POST['title']
    task.Description = request.POST['description']
    task.Priority = request.POST['priority']
    task.Due_date = request.POST['due_date']
    task.Status = request.POST['status']
    task.save()
    messages.success(request, 'Task Updated Successfully!')
    return redirect('/view_tasks_get/#aaa')

@login_required(login_url='/login_get/')
def delete_task(request,id):
    ob=Task.objects.get(id=id)
    ob.delete()
    messages.success(request, 'Task Deleted Successfully!')
    return redirect('/view_tasks_get/#aaa')
# Create your views here.
