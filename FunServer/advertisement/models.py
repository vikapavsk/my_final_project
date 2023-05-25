from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Article(models.Model):
    TYPE = (
        ('tanks', 'Танки'),
        ('heals', 'Хилы'),
        ('dd', 'ДД'),
        ('sellers', 'Торговцы'),
        ('guildmasters', 'Гилдмастеры'),
        ('questgivers', 'Квестгиверы'),
        ('smiths', 'Кузнецы'),
        ('tanners', 'Кожевники'),
        ('potions', 'Зельевары'),
        ('spellmasters', 'Мастера заклинаний'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_id = author.primary_key
    title = models.CharField(max_length=64)
    text = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=12, choices=TYPE, default='tanks', verbose_name='категория')
    upload = models.FileField(upload_to='uploads/')

    def __str__(self):
        return f'Объявление {self.pk}, Заголовок {self.title}'

    def preview(self):
        return self.text[0:123] + '...'

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])

    def get_categories():
        cats_list = [
        'Танки',
        'Хилы',
        'ДД',
        'Торговцы',
        'Гилдмастеры',
        'Квестгиверы',
        'Кузнецы',
        'Кожевники',
        'Зельевары',
        'Мастера заклинаний',
        ]
        return cats_list


class Response(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='responses')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=User)
    text = models.TextField('Текст отклика')
    publication_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f'{self.article.title} - {self.author.username} - {self.publication_date} - {self.text}'

    def approve(self):
        self.status = True
        self.save()

    def deny(self):
        self.status = False
        self.save()

    def get_absolute_url(self):
        return f'http://127.0.0.1:8000/article/{self.article.id}'

