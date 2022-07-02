from django.shortcuts import render, redirect
from .models import Word, ProfileUser
from django.views.generic import ListView
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login as dj_login, logout as dj_logout


class HomeView(ListView):
    model = Word
    template_name = 'words/index.html'
    context_object_name = 'words'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'WHAT..?'

        return ctx


class ProfileView(ListView):
    model = Word
    template_name = 'words/profile.html'
    context_object_name = 'words'


class СomplainView(ListView):
    model = Word
    template_name = 'words/сomplain.html'
    context_object_name = 'words'


class AddWord(ListView):
    model = Word
    template_name = 'words/add_word.html'
    context_object_name = 'words'


def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            dj_login(request, user)
            return redirect('main')
    else:
        form = LoginForm()

    return render(request, 'words/login.html', {'title': 'Логин', 'form': form})


def logout(request):
    dj_logout(request)
    return redirect('main')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_form = form.save()
            name = form['username'].value()
            ProfileUser.objects.create(name=User.objects.get(username=name))
            dj_login(request, user_form)
            return redirect('main')
        else:
            return redirect('register')
    else:
        print('Неудача')
        form = RegisterForm()

    return render(request, 'words/register.html', {'title': 'Регистрация', 'form': form})
