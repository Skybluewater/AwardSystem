from django.db import models
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
from django.utils import timezone
from mdeditor.fields import MDTextField
from apps.grade_info.models import SchoolYearInfo, MajorInfo
from apps.account.models import User
from database.base_model import BaseModel

# Create your models here.


class AwardInfo(models.Model):
    name = models.CharField(max_length=25, verbose_name="奖学金名称")
    SchoolYear = models.ForeignKey(SchoolYearInfo, on_delete=models.CASCADE)
    Major = models.ManyToManyField(MajorInfo, verbose_name="专业信息")
    ifHasClass = models.BooleanField(default=False, verbose_name="是否有等级")
    amount = models.IntegerField(verbose_name="奖学金总数")
    addition = MDTextField(verbose_name="附言")
    money = models.IntegerField(default=0, verbose_name="奖学金金额")


class AwardClassification(models.Model):
    firstClass = "f"
    secondClass = "s"
    thirdClass = "t"

    classChoice = (
        (firstClass, 'firstClass'),
        (secondClass, 'secondClass'),
        (thirdClass, 'thirdClass')
    )

    AwardInfo = models.ForeignKey("AwardInfo", on_delete=models.CASCADE)
    classification = models.CharField(max_length=1, choices=classChoice, null=True, blank=True, verbose_name="等级分类")
    amount = models.IntegerField(verbose_name="奖学金总数")
    money = models.IntegerField(default=0, verbose_name="奖学金金额")


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="奖学金分类")

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="奖学金等级")

    def __str__(self):
        return self.name


class AnswerPostBase(models.Model):
    title = models.CharField(max_length=70, verbose_name="标题")
    body = MDTextField(verbose_name="文章")
    created_time = models.DateTimeField(verbose_name="创建日期")
    modified_time = models.DateTimeField(verbose_name="修改日期")
    excerpt = models.CharField(max_length=200, blank=True, verbose_name="摘要")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0, verbose_name="浏览量")

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        ordering = ['-created_time']

    """ 1.reverse的'blog:detail'对应blog应用下的name='detail'的方法(对应urls.py的name)
        2.reverse()方法会去解析'blog:detail'的url,解析规则是根据urls.py里的正则.
        3.根据正则规则,解析结果为post/255/,这样Post自己就生成了自己的url
        4.kwargs表示按照关键字传值将多余的传值用字典形式呈现
    """

    def increase_views(self):
        # 该函数每被调用一次 views+1
        self.views += 1
        # 只更新数据库中views字段的值
        self.save(update_fields=['views'])

    # 摘要逻辑 重写save()方法,保存到数据库之前进行一次过滤
    def save(self, *args, **kwargs):
        self.created_time = timezone.now()
        self.modified_time = self.created_time
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(AnswerPostBase, self).save(*args, **kwargs)


class Post(AnswerPostBase):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    users_focus = models.ManyToManyField(User, related_name="articles_like", blank=True, verbose_name="用户关注")

    # 自定义获取路径方法
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})


""" 通过此模型获得post对应的多个奖学金 """


class AwardInfoPost(models.Model):
    AwardInfo = models.OneToOneField("AwardInfo", on_delete=models.CASCADE, verbose_name="奖学金信息")
    AwardPost = models.ForeignKey("Post", on_delete=models.CASCADE, verbose_name="奖学金Post信息")
