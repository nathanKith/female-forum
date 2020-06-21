from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from datetime import datetime
import os


class Tag(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


def avatar_upload_to(instance, filename):
    return os.path.join('uploads', instance.user.username + os.path.splitext(filename)[1])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', default='uploads/avatars/avatar.jpg')

    def __str__(self):
        return self.user.username


class QuestionManager(models.Manager):
    def hot(self):
        return self.order_by('-date')

    def best(self):
        return self.order_by('-rating')

    def tag_question(self, tag):
        return self.filter(tags__name=tag)


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=127, verbose_name=u"Заголовок вопрос")
    content = models.TextField(verbose_name='Вопрос')
    date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания вопроса")
    tags = models.ManyToManyField(Tag, blank=True)
    rating = models.IntegerField(default=0, verbose_name=u"Рейтинг вопроса")
    objects = QuestionManager()

    def answers_quantity(self):
        return Answer.objects.answer_quantity(self)


class AnswerManager(models.Manager):
    def answer_quantity(self, q):
        return self.filter(question=q).count()

    def question_answers(self, q):
        return self.filter(question=q)


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(verbose_name=u"Заголовок ответа")
    date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания ответа")
    rating = models.IntegerField(default=0, verbose_name=u"Рейтинг ответа")
    is_correct = models.BooleanField(default=False, verbose_name=u"Корректность вопроса")

    objects = AnswerManager()


class LikeQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    state = models.NullBooleanField(default=None)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)


class LikeAnswer(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    state = models.NullBooleanField(default=None)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
