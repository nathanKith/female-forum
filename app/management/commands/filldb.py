from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Question, Profile, Tag, Answer
from random import choice, randint, choices
from faker import Faker

f = Faker()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--authors', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--answers', type=int)
        parser.add_argument('--tags', type=int)

    def fill_profile(self, cnt):
        if cnt is None:
            return False
        for i in range(cnt):
            u = User(username=f.name())
            u.save()
            Profile.objects.create(
                user=u,
            )
        return True

    def fill_questions(self, cnt):
        if cnt is None:
            return False
        profile_ids = list(Profile.objects.values_list('id', flat=True))
        for i in range(cnt):
            question = Question.objects.create(
                author=Profile.objects.get(pk=choice(profile_ids)),
                title=f.word()[:60],
                content=f.text(),
            )
            tag_ids = list(Tag.objects.values_list('id', flat=True))
            tags = [
                Tag.objects.get(pk=i)
                for i in choices(
                    tag_ids,
                    k=randint(1, 3),
                )
            ]
            for tag in tags:
                question.tags.add(tag)
            # question.save()
        return True

    def fill_answers(self, cnt):
        if cnt is None:
            return False
        profile_ids = list(Profile.objects.values_list('id', flat=True))
        question_ids = list(Question.objects.values_list('id', flat=True))
        for i in range(cnt):
            Answer.objects.create(
                author=Profile.objects.get(pk=choice(profile_ids)),
                question=Question.objects.get(pk=choice(question_ids)),
                content=f.text(),
            )
        return True

    def fill_tags(self, cnt):
        if cnt is None:
            return False
        for i in range(cnt):
            Tag.objects.create(
                name=f.word(),
            )

    def handle(self, *args, **options):
        self.fill_profile(options.get('authors', 0))
        self.fill_questions(options.get('questions', 0))
        self.fill_answers(options.get('answers', 0))
        self.fill_tags(options.get('tags', 0))
