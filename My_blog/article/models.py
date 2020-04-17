from django.db import models
from django.contrib.auth.models import User   # Django内建的User模型
from django.urls import reverse
from django.utils import timezone   # timezone 用于处理时间相关业务

class ArticleColumn(models.Model):
    '''栏目model'''
    title = models.CharField(max_length=100, blank=True)    # 栏目标题
    created = models.DateTimeField(default=timezone.now)    # 创建时间

    def __str__(self):
        return self.title


# 博客文章数据模型
class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 文章作者。参数 on_delete 用户指定数据删除方式
    title = models.CharField(max_length=100)    # 文章标题
    body = models.TextField()   # 文章正文。保存大量文本使用TextField
    created = models.DateTimeField(default=timezone.now)    # 文章创建时间。参数default=timezone默认创建数据时的时间
    updated = models.DateTimeField(auto_now=True)   # 文章更新时间。参数auto_now=True指定每次数据更新时自动写入的时间
    total_views = models.PositiveIntegerField(default=0)    # 浏览量
    column = models.ForeignKey(ArticleColumn, null=True, blank=True, on_delete=models.CASCADE, related_name='article')

    class Meta: # 定义元数据
        # ordering 指定模型返回的数据的排列顺序
        # '-id' 表明数据应该以倒序排列
        ordering = ('-id',)    # ordering 是元祖，括号中只有一个元素时不要忘记末尾的逗号

    def __str__(self):  # 函数__str__定义当调用对象的str()方法时返回值内容
        return self.title   # 返回文章标题

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])





