from django.urls import path
from userprofile import views

app_name = 'userprofile'

urlpatterns = [
    path('login/', views.user_login, name='login'),  # 用户登陆
    path('logout/', views.user_logout, name='logout'),   # 用户注销
    path('register/', views.user_register, name='register'),    # 用户注册
    path('delete/<int:id>/', views.user_delete, name='delete'),   # 用户删除
    path('edit/<int:id>/', views.profile_edit, name='edit')     # 用户信息
]