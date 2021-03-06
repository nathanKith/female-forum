# Generated by Django 3.0.5 on 2020-06-14 10:48

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Заголовок ответа')),
                ('date', models.DateTimeField(default=datetime.datetime.now, verbose_name='Время создания ответа')),
                ('rating', models.IntegerField(default=0, verbose_name='Рейтинг ответа')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Корректность вопроса')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(default='uploads/default.jpeg', upload_to='uploads/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=127, verbose_name='Заголовок вопрос')),
                ('content', models.TextField(verbose_name='Вопрос')),
                ('date', models.DateTimeField(default=datetime.datetime.now, verbose_name='Время создания вопроса')),
                ('rating', models.IntegerField(default=0, verbose_name='Рейтинг вопроса')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Profile')),
                ('tags', models.ManyToManyField(blank=True, to='app.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='LikeQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='LikeAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Answer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Profile'),
        ),
    ]
