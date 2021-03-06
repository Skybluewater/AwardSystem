# Generated by Django 3.1.7 on 2021-04-10 06:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grade_info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AwardInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=25, verbose_name='奖学金名称')),
                ('ifHasClass', models.BooleanField(default=False, verbose_name='是否有等级')),
                ('amount', models.IntegerField(verbose_name='奖学金总数')),
                ('addition', mdeditor.fields.MDTextField(verbose_name='附言')),
                ('money', models.IntegerField(default=0, verbose_name='奖学金金额')),
                ('Major', models.ManyToManyField(to='grade_info.MajorInfo', verbose_name='专业信息')),
                ('SchoolYear', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grade_info.schoolyearinfo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='奖学金分类')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='奖学金等级')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, verbose_name='标题')),
                ('body', mdeditor.fields.MDTextField(verbose_name='文章')),
                ('created_time', models.DateTimeField(verbose_name='创建日期')),
                ('modified_time', models.DateTimeField(verbose_name='修改日期')),
                ('excerpt', models.CharField(blank=True, max_length=200, verbose_name='摘要')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='浏览量')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='award_info.category')),
                ('tags', models.ManyToManyField(blank=True, to='award_info.Tag')),
                ('users_focus', models.ManyToManyField(blank=True, related_name='articles_like', to=settings.AUTH_USER_MODEL, verbose_name='用户关注')),
            ],
            options={
                'ordering': ['-created_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AwardInfoPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AwardInfo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='award_info.awardinfo', verbose_name='奖学金信息')),
                ('AwardPost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='award_info.post', verbose_name='奖学金Post信息')),
            ],
        ),
        migrations.CreateModel(
            name='AwardClassification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('classification', models.CharField(blank=True, choices=[('f', 'firstClass'), ('s', 'secondClass'), ('t', 'thirdClass')], max_length=1, null=True, verbose_name='等级分类')),
                ('amount', models.IntegerField(verbose_name='奖学金总数')),
                ('money', models.IntegerField(default=0, verbose_name='奖学金金额')),
                ('AwardInfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='award_info.awardinfo')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
