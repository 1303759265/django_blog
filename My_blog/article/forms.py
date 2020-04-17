from django import forms    # 引入表单类
from .models import ArticlePost     # 引入文章模型


# 写文章的表单类
class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost     # 指明数据模型来源
        fields = ('title', 'body')  # 定义表单包含字段