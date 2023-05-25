from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from django.views.generic.edit import FormMixin
from .models import Article, Response
from .forms import ArticleForm, EditForm, ResponseForm
from .filters import ArticleFilter


class ArticlesList(ListView):
    model = Article
    ordering = '-publication_date'
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ArticleFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context



# class ArticlesList(ListView):
#     model = Article
#     ordering = '-publication_date'
#     template_name = 'articles.html'
#     context_object_name = 'articles'
#     paginate_by = 5

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['time_now'] = datetime.utcnow()
    #     return context

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = ArticleFilter(self.request.GET, queryset)
    #     return self.filterset.qs
    #



    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['filterset'] = self.filterset
    #     return context


class ArticlesByUser(LoginRequiredMixin, ListView):
    ''' List of all posts posted by current User - author of posts '''
    ''' Also applied filter - search responses/comments by author's posts '''
    model = Article
    template_name = 'articles_by_user.html'
    context_object_name = 'articles_by_user'
    ordering = ['-publication_date']

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user).order_by('-publication_date')

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
        context = super().get_context_data(**kwargs)
        author = self.request.user
        author_posts = Article.objects.filter(author=author).order_by('-publication_date')
        cats_list = Article.get_categories()
        context['cats_list'] = cats_list
        context['author_posts'] = author_posts
        context['filter'] = ArticleFilter(self.request.GET,
                                       queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context



def CategoryView(request, cats):
    articles_by_category = Article.objects.filter(category=cats.replace('-', ' ')).order_by('-publication_date')
    cats_list = Article.get_categories()
    return render(request, 'categories.html', {'cats': cats.title().replace('-', ' '), 'articles_by_category': articles_by_category, 'cats_list': cats_list})


class ArticleDetail(DetailView):
    model = Article
    template_name = 'article.html'
    context_object_name = 'article'

    # def get_success_url(self):
    #     return reverse_lazy('article_detail', kwargs={'pk': self.get_object().id})

    def get_context_data(self, *args, **kwargs):
        cats_list = Article.get_categories()
        context = super(DetailView, self).get_context_data(*args, **kwargs)

        article_now = get_object_or_404(Article, id=self.kwargs['pk'])
        article_responses = article_now.responses.order_by('-publication_date')
        article_responses.count = article_now.responses.count()

        context['article_responses.count'] = article_responses.count
        context['article_responses'] = article_responses
        context['cats_list'] = cats_list
        return context


class ArticleCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = ArticleForm
    model = Article
    template_name = 'article_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    raise_exception = True
    form_class = ArticleForm
    model = Article
    template_name = 'article_edit.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs


class ArticleDelete(LoginRequiredMixin, DeleteView):
    raise_exception = True
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('articles')



class ResponseCreate(LoginRequiredMixin, CreateView):
    ''' Creation of a new response/comment by logged-in user '''
    model = Response
    form_class = ResponseForm
    template_name = 'response_create.html'

    def form_valid(self, form):
        ''' Autosaving current logged in user as comment's author after creating this new comment '''
        form.instance.author = self.request.user
        form.instance.article_id = self.kwargs['pk']  # забираем pk текущего поста
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        ''' Getting menue list of all post's categories for dropdown menue "Categories" in navbar '''
        cats_list = Article.get_categories()
        context = super(CreateView, self).get_context_data(*args, **kwargs)
        context['cats_list'] = cats_list
        return context

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.kwargs['pk']})


@login_required
def response_approve(request, pk):
    ''' Accept response - Button on 'article-detail' and 'dashboard' pages'''
    response = get_object_or_404(Response, pk=pk)
    response.approve()
    return redirect('article_detail', pk=response.article.pk)


@login_required
def response_deny(request, pk):
    ''' Unaccept response and remove approvement - Button on 'article-detail' and 'dashboard' pages'''
    response = get_object_or_404(Response, pk=pk)
    response.disapprove()
    return redirect('article_detail', pk=response.article.pk)


@login_required
def response_delete(request, pk):
    ''' Delete comment - Button on 'article-detail' and 'dashboard' pages'''
    response = get_object_or_404(Response, pk=pk)
    response.delete()
    return redirect('article_detail', pk=response.article.pk)














# @login_required
# def news_subscribe(request, pk):
#     ''' Weekly news and digest subscription - Button in Footer ('main.html' page) '''
#     userprofile = get_object_or_404(UserProfile, user_id=request.user.id)
#     userprofile.subscribe()
#     user_name = request.user.username
#     email = request.user.email
#     subscribe_confirmation_message.delay(user_name, email)  # email subscription confirmation by Celery (tasks.py)
#     return redirect('home')




# class ResponsesList(LoginRequiredMixin, ListView):
#     raise_exception = True
#     model = Response
#     template_name = 'response_page.html'
#     context_object_name = 'responses'
#
#     def get_queryset(self):
#         queryset = Response.objects.filter(author=self.request.user).all()
#         return queryset
#
#
# class ArticleResponsesList(LoginRequiredMixin, ListView):
#     raise_exception = True
#     model = Response
#     template_name = 'article_response_list.html'
#     context_object_name = 'article_response_list'
#
#     def get_queryset(self):
#         queryset = Response.objects.filter(article__author=self.request.user).all()
#         return queryset
#
#     def get_queryset(self):
#         queryset = Response.objects.filter(article__author=self.request.user).order_by('-id').all()
#         self.filterset = ArticleResponseFilter(self.request.GET, queryset)
#         self.filterset.form.fields['article'].queryset = Article.objects.filter(author=self.request.user)
#         return self.filterset.qs
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['filterset'] = self.filterset
#         return context
#
# @login_required
# def accept(request, **kwargs):
#     response = Response.objects.get(id=kwargs.get('pk'))
#     response.status = True
#     response.save()
#     return redirect(request.META.get('HTTP_REFERER'))
#
#
# @login_required
# def deny(request, **kwargs):
#     response = Response.objects.get(id=kwargs.get('pk'))
#     response.delete()
#     return redirect(request.META.get('HTTP_REFERER'))
