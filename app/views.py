from django.shortcuts import render
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.models import Question, Answer, Profile, Tag, LikeAnswer, LikeQuestion


tags_and_users = {
    'tags': Tag.objects.values_list('name', flat=True),
    'best_users': [i.user.username for i in Profile.objects.all()],
}


def pagination(object_list, request, per_page=20):
    p = request.GET.get('page')
    pages = Paginator(object_list, per_page)

    try:
        content = pages.page(p)
    except PageNotAnInteger:
        content = pages.page(1)
    except EmptyPage:
        content = pages.page(pages.num_pages)

    return content, p


def main(request):
    content, page = pagination(Question.objects.hot(), request)
    return render(request, 'index.html', {
        'title': 'new questions',
        'page': page,
        'questions': content,
        **tags_and_users,
    })


def best_questions(request):
    content, page = pagination(Question.objects.best(), request)
    return render(request, 'index.html', {
        'title': 'best questions',
        'page': page,
        'questions': content,
        **tags_and_users,
    })


def tag_questions(request, cur_tag):
    content, page = pagination(Question.objects.tag_question(cur_tag), request)
    return render(request, 'index.html', {
        'title': f'question about {cur_tag}',
        'page': page,
        'questions': content,
        **tags_and_users,
    })


def question(request, qid):
    content, page = pagination(
        Answer.objects.question_answers(Question.objects.get(pk=qid)),
        request,
        per_page=5,
    )
    return render(request, 'question.html', {
        'question': Question.objects.get(pk=qid),
        'answers': content,
        'page': page,
        **tags_and_users,
    })


def login(request):
    return render(request, 'signin.html', tags_and_users)


def signup(request):
    return render(request, 'signup.html', tags_and_users)


def ask(request):
    return render(request, 'ask.html', tags_and_users)
