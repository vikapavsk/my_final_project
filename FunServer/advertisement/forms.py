from django import forms
from django.core.exceptions import ValidationError
from .models import Article, Response


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['author',
                  'category',
                  'title',
                  'text',
                  'upload',
                  ]
        labels = {
            'author': 'Автор',
            'category': 'Категория',
            'title': 'Заголовок',
            'text': 'Содержание',
            'upload': 'Файл',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        if title is not None and len(title) < 5:
            raise ValidationError({
                "title": "Название не может быть менее 5 символов."
            })
        return cleaned_data


class EditForm(forms.ModelForm):
    fields = ['author',
              'category',
              'title',
              'text',
              'upload',
              ]
    labels = {
        'author': 'Автор',
        'category': 'Категория',
        'title': 'Заголовок',
        'text': 'Текст',
        'upload': 'Файл',
    }
    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок'}),
        'category': forms.Select(attrs={'class': 'form-control'}),
        'text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ('text', )

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите Ваш отклик ...'}),
        }
