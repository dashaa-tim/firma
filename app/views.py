"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .forms import AnketaForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db import models
from .models import Blog
from .models import Comment # использование модели комментариев
from .forms import CommentForm # использование формы ввода комментария
from .forms import AnketaForm
from .forms import BlogForm


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная страница ',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты ',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас ',
            'message':'Вас приветствует турфирма "ВэлТур+!"',
            'year':datetime.now().year,
        }
    )

def links(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ресурсы ',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def anketa(request):
    assert isinstance(request, HttpRequest)
    data = None
    dov = {'1': 'Очень доволен/льна', '2':'Доволен/льна', '3':'Скорее доволен/льна', '4':'Скорее недоволен/льна', '5':'Недоволен/льна', '6':'Очень недоволен/льна'}
    rek = {'1':'Несомненно да', '2':'Вероятно да', '3':'Я не знаю', '4':'Вероятно нет', '5':'Несомненно нет'}
    avto = {'1': 'Да' , '2': 'Ещё думаю', '3': 'Нет'}
    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['dov'] = dov[ form.cleaned_data['dov'] ]
            data['rek'] = rek[ form.cleaned_data['rek'] ]
            data['avto'] = avto[ form.cleaned_data['avto'] ]
            if(form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            form = None
    else:
         form = AnketaForm()
    return render(
        request,
        'app/anketa.html',
        {
            'form':form,
            'data':data
            }
        )

def registration(request):
    """Renders the registration page."""

    if request.method == "POST": # после отправки формы
        regform = UserCreationForm(request.POST)
        if regform.is_valid(): #валидация полей формы
            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
            reg_f.is_staff = False # запрещен вход в административный раздел
            reg_f.is_active = True # активный пользователь
            reg_f.is_superuser = False # не является суперпользователем
            reg_f.date_joined = datetime.now() # дата регистрации
            reg_f.last_login = datetime.now() # дата последней авторизации

            reg_f.save() # сохраняем изменения после добавления данных

            return redirect('home') # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
        'regform': regform, # передача формы в шаблон веб-страницы

        'year':datetime.now().year,
        }

)

def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all() # запрос на выбор всех статей блога из модели
    return render(
        request,
        'app/blog.html',
        {
        'title':'Блог ',
        'posts': posts, # передача списка статей в шаблон веб-страницы
        'year':datetime.now().year,
        }

)

def blogpost(request, parametr):
    """Renders the blogpost page."""
    post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr)
       
    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
            comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save() # сохраняем изменения после добавления полей
            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
      form = CommentForm() # создание формы для ввода комментария
      assert isinstance(request, HttpRequest)     
      return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы
            'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
            'form': form, # передача формы добавления комментария в шаблон веб-страницы
            'year':datetime.now().year,
        }
)

def newpost(request):
    """Renders the newpost page."""

    if request.method == "POST":                        #после отправки формы
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()

            blog_f.save()

            return redirect('blog')
    else:
        blogform = BlogForm()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            
            'year': datetime.now().year,
        }
    )

def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео ',
            'message':'Приятного просмотра!',
            'year':datetime.now().year,
              }
    )

def tyr(request):
    """Renders the tyr page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/tyr.html',
        {
            'title':'Туры ',
            'message':'',
            'year':datetime.now().year,
        }
    )

def turkey(request):
    """Renders the turkey page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/turkey.html',
        {
            'title':'Турция',
            'message':' ',
            'year':datetime.now().year,
        }
    )

def russia(request):
    """Renders the russia page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/russia.html',
        {
            'title':'Россия',
            'message':' ',
            'year':datetime.now().year,
        }
    )

def tunisia(request):
    """Renders the tunisia page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/tunisia.html',
        {
            'title':'Тунис',
            'message':' ',
            'year':datetime.now().year,
        }
    )

def greece(request):
    """Renders the greece page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/greece.html',
        {
            'title':'Греция',
            'message':' ',
            'year':datetime.now().year,
        }
    )

def spain(request):
    """Renders the spain page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/spain.html',
        {
            'title':'Испания',
            'message':' ',
            'year':datetime.now().year,
        }
    )

def cyprus(request):
    """Renders the cyprus page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/cyprus.html',
        {
            'title':'Кипр',
            'message':' ',
            'year':datetime.now().year,
        }
    )