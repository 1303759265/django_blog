import markdown
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ArticlePostForm
from article.models import ArticlePost, ArticleColumn
from django.contrib.auth.models import User
from django.core.paginator import Paginator # 分页
from django.db.models import Q  # Q对象
from comment.models import Comment


# 文章列表
def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    # 用户逻辑搜索
    if search:
        if order == 'total_views':
            # 用Q对象进行联合搜索
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search)  |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        # 将search参数重置为空
        search = ''
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()

    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context = {'articles':articles, 'order':order, 'search':search}
    return render(request, 'article/list.html', context)

# 文章详情
def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)    # 取出相应的文章
    article.total_views += 1
    article.save(update_fields=['total_views'])
    comments = Comment.objects.filter(article=id)
    md = markdown.Markdown(
        extensions = [
            'markdown.extensions.extra',    # 包含缩写 表格等常用扩展
            'markdown.extensions.codehilite',   # 语法高亮扩展
            # 目录扩展
            'markdown.extensions.toc',
        ])
    article.body = md.convert(article.body)
    context = {'article':article, 'toc':md.toc, 'comments':comments}   # 需要传递给模板的对象
    return render(request, 'article/detail.html', context)


# 编写文章
def article_create(request):
    if request.method == 'POST':    # 判断用户请求是否是提交数据
        article_post_form = ArticlePostForm(data=request.POST)  # 将提交的数据赋值到表单实例中
        if article_post_form.is_valid():    # 判断提交的数据是否满足模型要求
            new_article = article_post_form.save(commit=False)  # 保存数据，但暂时不保存到数据库
            # 指定数据库 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            new_article.save()  # 将新文章保存到数据库中
            return redirect('article:article_list')     # 完成后返回文章列表
        else:   # 如果数据不合法，返回错误信息
            return HttpResponse('表单内容有误，请重新输入')

    else:   # 如果用户是请求数据
        article_post_form = ArticlePostForm()   # 创建表单实例
        columns = ArticleColumn.objects.all()
        context = { 'article_post_form': article_post_form, 'columns':columns }    # 赋值上下文
        return render(request, 'article/create.html', context)


# 删除文章
def article_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)    # 根据id获取需要删除的文章
        article.delete()    # 调用.delete()删除文章
        return redirect('article:article_list')     # 返回文章列表
    else:
        return HttpResponse('仅允许post请求')


# 安全删除
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        if request.user.id != article.author_id:
            return HttpResponse('你无权限删除这篇文章')
        article.delete()
        return redirect('article:article_list')
    else:
        return HttpResponse('仅允许POST请求')


# 更新文章
def article_update(request, id):
    '''
    通过post方法提交表单，更新title，body字段
    get方法进入初始化表单界面
    '''
    article = ArticlePost.objects.get(id=id)  # 获取需要修改的具体文章对象
    if request.user.id != article.author_id:
        return HttpResponse('你无权限修改这篇文章')
    if request.method == 'POST':    # 判断是否是post请求
        article_post_form = ArticlePostForm(data=request.POST)  # 将提交的表单数据赋值到表单实例中
        if article_post_form.is_valid():    # 判断提交的数据是否满足模型要求
            # 保存新写入的title和body
            article.title = request.POST['title']
            article.body = request.POST['body']
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            article.save()
            return redirect('article:article_detail', id=id) # 完成后返回修改后的文章中，需传入文章id
        else:   # 如果数据不合法
            return HttpResponse('提交的表单信息有误，请重新填写')
    else:   # 如果用户是GET请求
        article_post_form = ArticlePostForm()   # 创建表单实例
        columns = ArticleColumn.objects.all()
        # 赋值上下文，将article文章对象也传递进去，更新旧类容
        context = {'article':article, 'article_post_form':article_post_form, 'columns':columns,}
        return render(request, 'article/update.html', context)
