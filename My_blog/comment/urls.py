from django.urls import path
from comment import views

app_name = 'comment'

urlpatterns = [
    path('post-comment/<int:article_id>/', views.post_comment, name='post_comment'),    # 发表评论
]