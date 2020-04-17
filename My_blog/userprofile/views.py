from django.http import HttpResponse
from django.shortcuts import render, redirect
from userprofile.forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required   # 验证登陆的装饰器
from .forms import ProfileForm
from .models import Profile


# 用户登陆
def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data    # .cleaned_data 清洗出合法数据
            # 检测账号密码是否正确匹配到数据库的某个用户
            # 如果均匹配则返回这个user对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:    # 将用户数据保存在session中，即实现了登陆动作
                login(request, user)
                return redirect('article:article_list')
            else:
                return HttpResponse('您输入的账号或密码有误，请重新输入')
        else:
            return HttpResponse('您输入的账号或密码不合法')
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form':user_login_form}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse('请使用GET或POST请求')


# 用户注销
def user_logout(request):
    logout(request)
    return redirect('article:article_list')


# 用户注册
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])  # 设置密码
            new_user.save()
            login(request, new_user)
            return redirect('article:article_list')
        else:
            return HttpResponse('注册表单输入有误，请重新输入')
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form':user_register_form}
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse('请使用GET或POST请求数据')


# 删除用户
@login_required(login_url='/userprofile/login')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)  # 验证登陆用户和待删除用户是否相同
        if request.user == user:
            logout(request)
            user.delete()
            return redirect('article:article_list')
        else:
            return HttpResponse('您没有删除操作的权限')
    else:
        return HttpResponse('仅接受POST请求')


# 编辑用户信息
@login_required(login_url='/userprofile/login') # 要求用户登陆
def profile_edit(request, id):
    user = User.objects.get(id=id)
    # profile = Profile.objects.get(user_id=id)   # user_id 是 OneToOneField 自动生成的
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        if request.user != user:    # 验证修改数据者是否是本人
            return HttpResponse('您没有权限执行此操作')

        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_cd = profile_form.cleaned_data  # 取得清洗后的合法数据
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            if 'avatar' in request.FILES:   # 如果request.FILES存在文件，则保存
                profile.avatar = profile_cd['avatar']
            profile.save()
            return redirect('userprofile:edit', id=id)
        else:
            return HttpResponse('注册表单信息有误,请重新输入')
    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = {'profile_form': profile_form, 'profile':profile, 'user':user}
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse('只能使用GET或POST访问')