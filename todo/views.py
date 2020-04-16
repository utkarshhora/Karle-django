from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm, RegisterForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.
def home(request):
    """ Homepage """
    return render(request, 'todo/home.html')


def signupuser(request):
    """ Signup User """
    if request.user.is_authenticated:
        return redirect('currenttodos')
    else:
        if request.method == 'GET':
            return render(request, 'todo/signupuser.html', {'form':RegisterForm()})
        else:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect('currenttodos')
                except IntegrityError:
                    return render(request, 'todo/signupuser.html', {'form':RegisterForm(), 'error': 'Username already exists'})
            else:
                return render(request, 'todo/signupuser.html', {'form':RegisterForm(), 'error': 'Passwords do not match'})


@login_required
def currenttodos(request):
    """ List current todos """
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})


@login_required
def viewTodo(request, todo_id):
    """ View a particular todo """
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewTodo.html', {'todo':todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewTodo.html', {'todo':todo, 'form': form, 'error':'Invalid Input'})


def logoutuser(request):
    """ Logout user """
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def loginuser(request):
    """ Login User """
    if request.user.is_authenticated:
        return redirect('currenttodos')

    else:
        if request.method == 'GET':
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
        else:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error': 'Invalid Credentials'})
            else:
                login(request, user)
                return redirect('currenttodos')


@login_required
def createtodo(request):
    """ Create a todo """
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'error': 'Invalid Input', 'form': TodoForm()})


@login_required
def completeTodo(request, todo_id):
    """ Complete a Todo """
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deleteTodo(request, todo_id):
    """ Delete a Todo """
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')


@login_required
def completedTodos(request):
    """ List completed Todos """
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedTodos.html', {'todos': todos})


def test(request):
    """Test page"""
    return render(request, 'todo/test.html')
