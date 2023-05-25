from django.urls import path
from . import views
from .views import ArticlesList, ArticleDetail, ArticleCreate, ArticleUpdate, ArticleDelete, CategoryView, \
    ResponseCreate, ArticlesByUser


urlpatterns = [
    path('', ArticlesList.as_view(), name='articles_list'),
    path('<int:pk>', ArticleDetail.as_view(), name='article_detail'),
    path('create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
    path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('category/<str:cats>/', CategoryView, name='category'),
    path('<int:pk>/response/', ResponseCreate.as_view(), name='response_create'),
    path('response/<int:pk>/approve/', views.response_approve, name='response_approve'),
    path('response/<int:pk>/deny/', views.response_deny, name='response_deny'),
    path('response/<int:pk>/delete/', views.response_delete, name='response_delete'),
    path('articlesbyuser/', ArticlesByUser.as_view(), name='articles_by_user'),
    # path('user/<int:pk>/subscribe/', views.news_subscribe, name='news_subscribe'),
]
#
# urlpatterns = [
#    path('', ArticlesList.as_view(), name='articles_list'),
#    path('<int:pk>', ArticleDetail.as_view(), name='article_detail'),
#    path('create/', ArticleCreate.as_view(), name='article_create'),
#    path('<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
#    path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
#    path('responses_page/', ResponsesList.as_view(), name='responses'),
# ]
#
# path('article_responses/', ArticleResponsesList.as_view(), name='article_responses'),
# path('article_responses/accept/<int:pk>', accept, name='responses_accept'),
# path('article_responses/delete/<int:pk>', deny, name='responses_delete'),