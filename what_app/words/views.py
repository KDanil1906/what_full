from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import Word, ProfileUser, Complaint
from django.views.generic import ListView
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, AddWordForm, ProfileUpdate, ComplaintForm
from django.contrib.auth import login as dj_login, logout as dj_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(ListView):
    model = Word
    template_name = 'words/index.html'
    context_object_name = 'words'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'WHAT..?'

        return ctx


class ProfileView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'words/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = ProfileUpdate(instance=self.request.user)
        ctx['user'] = User.objects.get(username=self.request.user)
        ctx['words'] = []

        have_same_words = Word.objects.all().filter(user_id=ProfileUser.objects.get(name=self.request.user))
        if have_same_words.exists():
            ctx['words'] = have_same_words

        return ctx

    # def post(self, request, *args, **kwargs):
    #     profile_for = ProfileUpdate(self.request.POST, instance=self.request.user)
    #
    #     if profile_for.is_valid():
    #         profile_for.save()
    #
    #         return redirect('profile')
    #     else:
    #         messages.error(self.request, 'Что то пошло не так')
    #
    #     return redirect('profile')


class Search(ListView):
    template_name = 'words/index.html'
    context_object_name = 'words'
    paginate_by = 2

    def get_queryset(self):
        all_words = Word.objects.all()

        # Looking for word matches
        by_name = all_words.filter(word__icontains=self.request.GET.get('s'))
        # Looking for a match for the author
        authors = User.objects.filter(username__icontains=self.request.GET.get('s'))
        authors = ProfileUser.objects.filter(name__in=authors)
        by_author = all_words.filter(user_id__in=authors)
        # table consolidation
        total_sample = by_name.union(by_author)

        return total_sample

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Поиск'
        ctx['s'] = f"s={self.request.GET.get('s')}&"

        return ctx


class СomplainView(LoginRequiredMixin, ListView):
    template_name = 'words/сomplain.html'
    context_object_name = 'word'

    def get_queryset(self):
        return Word.objects.get(id=self.kwargs['id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Жалоба'
        ctx['form'] = ComplaintForm()

        return ctx

    def post(self, request, *args, **kwargs):
        form = ComplaintForm(request.POST)

        if form.is_valid():
            user_id = ProfileUser.objects.get(name=User.objects.get(id=self.request.user.id))
            word_id = Word.objects.get(id=self.kwargs['id'])
            explanation = request.POST['complaint']

            Complaint.objects.create(
                user_id=user_id,
                word_id=word_id,
                explanation=explanation
            )
            print(user_id)
            print(word_id)

            return redirect('main')
        else:
            messages.error(self.request, 'Что то пошло не так')

        return redirect('main')


@login_required
def add_word(request):
    if request.method == 'POST':
        form = AddWordForm(data=request.POST)
        if form.is_valid():
            user = ProfileUser.objects.get(name=request.user)
            word = form['word'].value()
            definition = form['definition'].value()
            example = form['example'].value()
            try:
                Word.objects.create(
                    user_id=user,
                    word=word,
                    definition=definition,
                    example=example
                )
                messages.success(request, 'Слово успешно добавлено')
                return redirect('add_word')
            except IntegrityError:
                messages.error(request, 'Такое слово уже существует')
                return redirect('add_word')

            print(word, definition, example)

    else:
        form = AddWordForm()

    return render(request, 'words/add_word.html', {'title': 'Добавить слово', 'form': form})


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
