from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import Word, ProfileUser, Complaint, Favorite, UsersMarks
from django.views.generic import ListView
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, AddWordForm, ComplaintForm, NameUserUpdate
from django.contrib.auth import login as dj_login, logout as dj_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


class HomeView(ListView):
    model = Word
    template_name = 'words/index.html'
    context_object_name = 'words'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'WHAT..?'

        ordering_db = {}
        if self.request.user.is_authenticated:
            user_id = ProfileUser.objects.get(name=User.objects.get(username=self.request.user))
            favorite_id = Favorite.objects.filter(user_id=user_id).select_related().all()
            print(favorite_id)

        ordering_db = Word.objects.all()
        print(ordering_db)

        return ctx

    def get_queryset(self):
        return Word.objects.all().order_by('-id')


class ProfileView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'words/profile.html'
    context_object_name = 'words'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['form'] = NameUserUpdate(instance=self.request.user)
        ctx['user'] = User.objects.get(username=self.request.user)

        return ctx

    def get_queryset(self):
        result_db = {}
        have_same_words = Word.objects.all().filter(
            user_id=ProfileUser.objects.get(name=self.request.user)).select_related()
        if have_same_words.exists():
            result_db = have_same_words.order_by('-id')
        return result_db

    def post(self, request, *args, **kwargs):
        profile_for = NameUserUpdate(self.request.POST ,instance=self.request.user)

        if profile_for.is_valid():
            profile_for.save()

            print('Данные хороши')
            return redirect('profile')
        else:
            messages.error(self.request, 'Аккаунт с таким именем уже существует')

        return redirect('profile')


class Search(ListView):
    template_name = 'words/index.html'
    context_object_name = 'words'
    paginate_by = 2

    def get_queryset(self):
        print(self.request)
        total_sample = {}

        if self.kwargs['type'] == 'input':
            all_words = Word.objects.all()

            # Looking for word matches
            by_name = all_words.filter(word__icontains=self.request.GET.get('s'))
            # Looking for a match for the author
            authors = User.objects.filter(username__icontains=self.request.GET.get('s'))
            authors = ProfileUser.objects.filter(name__in=authors)
            by_author = all_words.filter(user_id__in=authors)
            # table consolidation
            total_sample = by_name.union(by_author)
        elif self.kwargs['type'] == 'word':
            total_sample = Word.objects.filter(word__icontains=self.kwargs['value'])
        elif self.kwargs['type'] == 'author':
            user_id = ProfileUser.objects.get(name=User.objects.get(username=self.kwargs['value']))
            total_sample = Word.objects.filter(user_id=user_id)

        return total_sample

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Поиск'
        ctx['s'] = f"s={self.request.GET.get('s')}&"

        return ctx


class OrderingView(ListView):
    model = Word
    template_name = 'words/index.html'
    context_object_name = 'words'
    paginate_by = 2

    def get_queryset(self):
        ordering_db = []

        if self.kwargs['kind'] == 'random':
            ordering_db = Word.objects.all().order_by('?')
            print(ordering_db)
        elif self.kwargs['kind'] == 'favorite':
            user_id = ProfileUser.objects.get(name=User.objects.get(username=self.request.user))
            favorite_id = Favorite.objects.select_related('word_id').filter(user_id=user_id).select_related().all()
            print(favorite_id)
            for i in favorite_id:
                print(i.word_id.like)
                ordering_db.append(i.word_id)

            print(ordering_db)
        return ordering_db

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.kwargs['kind'] == 'random':
            ctx['title'] = 'WHAT'
        elif self.kwargs['kind'] == 'favorite':
            ctx['title'] = 'favorite'

        return ctx


def favorite(request, id):
    data = {}
    user_id = ProfileUser.objects.get(name=User.objects.get(id=request.user.id))
    word_id = Word.objects.get(id=id)
    all_favorites = Favorite.objects.all()

    if all_favorites.filter(user_id=user_id, word_id=word_id).exists():
        all_favorites.filter(user_id=user_id, word_id=word_id).delete()
    else:
        all_favorites.create(
            user_id=user_id,
            word_id=word_id
        )

    return JsonResponse({'data': data})


@login_required
def marks(request, id, mark):
    data = {}
    identify_mark = {
        0: 'like',
        1: 'dislike'
    }

    all_words = Word.objects.all()
    user_id = ProfileUser.objects.get(name=User.objects.get(id=request.user.id))
    word_id = all_words.get(id=id)
    all_marks = UsersMarks.objects.all()

    if all_marks.filter(user_id=user_id, word_id=word_id).exists():
        word_mark = all_marks.filter(user_id=user_id, word_id=word_id).first()
        user_mark = word_mark.mark
        if user_mark == bool(mark):
            print(word_id.like)
            if bool(mark):
                word_id.dislike -= 1
            else:
                word_id.like -= 1
            word_id.save()

            word_mark.delete()
        else:
            if bool(mark):
                word_id.like -= 1
                word_id.dislike += 1
            else:
                word_id.like += 1
                word_id.dislike -= 1

            word_id.save()

            word_mark.mark = bool(mark)
            word_mark.save()
    else:
        all_marks.create(
            user_id=user_id,
            word_id=word_id,
            mark=bool(mark)
        )

        if bool(mark):
            word_id.dislike += 1
        else:
            word_id.like += 1
        word_id.save()

    return JsonResponse({'data': data})


class ComplainView(LoginRequiredMixin, ListView):
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
