from django.shortcuts import render, redirect
from .models import Word, ProfileUser
from django.views.generic import ListView
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth import login
from datetime import date


class HomeView(ListView):
    model = Word
    template_name = 'words/index.html'
    context_object_name = 'words'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'WHAT..?'

        return ctx


def login(request):
    if request.method == 'POST':
        pass
    else:
        form = RegisterForm()

    return render(request, 'words/login.html', {'title': 'Логин'})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            name = form['username'].value()
            password = form['password1'].value()
            today = str(date.today())
            ProfileUser.objects.create(name=User.objects.get(username=name))
            login(form)
            return redirect('main')
        else:
            print('что то не то')
            # print(form)
            pass
    else:
        print('Неудача')
        form = RegisterForm()

    return render(request, 'words/register.html', {'title': 'Регистрация', 'form': form})
