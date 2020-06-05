"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.db import models
from .models import Comment
from.models import Blog

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

class AnketaForm(forms.Form):
    name = forms.CharField(label='Ваше имя', min_length=2, max_length=100)
    dov = forms.ChoiceField(label='Насколько Вы довольны нашим веб-сайтом?',
                               choices=[('1','Очень доволен/льна'), ('2','Доволен/льна'), ('3','Скорее доволен/льна'), ('4','Скорее недоволен/льна'), ('5','Недоволен/льна'), ('6','Очень недоволен/льна')],
                               widget=forms.RadioSelect, initial=1)
    rek = forms.ChoiceField(label='Вы бы рекомендовали наш веб-сайт другим людям?',
                               choices=[('1','Несомненно да'), ('2','Вероятно да'), ('3','Я не знаю'), ('4','Вероятно нет'), ('5','Несомненно нет')],
                               widget=forms.RadioSelect, initial=1)
    avto = forms.ChoiceField(label='Собираетесь ли вы путешествовать в ближайшее время?',
                               choices=(('1','Да'), 
                                        ('2','Ещё думаю'),
                                        ('3','Нет')), initial=1)
    notice = forms.BooleanField(label='Получать новости сайта на e-mail?',
                                required=False)
    email = forms.EmailField(label='Ваш e-mail', min_length=7)
    message = forms.CharField(label='Оставьте свой отзыв:',
                              widget=forms.Textarea(attrs={'rows':10, 'cols':40}))

class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment # используемая модель
        fields = ('text',) # требуется заполнить только поле text
        labels = {'text': "Комментарий"} # метка к полю формы text

class BlogForm (forms.ModelForm):
    class Meta:
        model = Blog #используемая модель
        fields = ('title', 'description', 'content', 'posted', 'author', 'image',)
        labels = {'title':"Заголовок",'description':"Краткое описание", 'content':"Содержание", 'posted':"Дата", 'author':"Автор", 'image':"Изображение",}