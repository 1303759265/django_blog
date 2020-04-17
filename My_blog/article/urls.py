from django.urls import path

from article import views

app_name = 'article'

urlpatterns =[
    path('article-list/', views.article_list, name='article_list'),     # 文章列表
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),   # 文章详情
    path('article-create/', views.article_create, name='article_create'),   # 写文章
    path('article-delete/<int:id>/', views.article_delete, name='article_delete'),   # 删除文章
    path('article_safe_delete/<int:id>/',views.article_safe_delete, name='article_safe_delete'),    # 安全删除文章
    path('article-update/<int:id>/', views.article_update, name='article_update'),   #更新文章
]