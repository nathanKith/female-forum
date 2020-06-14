from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from datetime import datetime


class Tag(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='uploads/', default='static/img/avatar.jpg')

    def __str__(self):
        return self.user.username


class QuestionManager(models.Manager):
    def hot(self):
        return self.order_by('-date')

    def best(self):
        return self.order_by('-rating')

    def tag_question(self, tag):
        return self.filter(tags=tag)


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=127, verbose_name=u"Заголовок вопрос")
    content = models.TextField(verbose_name='Вопрос')
    date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания вопроса")
    tags = models.ManyToManyField(Tag, blank=True)
    rating = models.IntegerField(default=0, verbose_name=u"Рейтинг вопроса")
    objects = QuestionManager()


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(verbose_name=u"Заголовок ответа")
    date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания ответа")
    rating = models.IntegerField(default=0, verbose_name=u"Рейтинг ответа")
    is_correct = models.BooleanField(default=False, verbose_name=u"Корректность вопроса")


class LikeQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    state = models.NullBooleanField(default=None)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)


class LikeAnswer(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    state = models.NullBooleanField(default=None)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
