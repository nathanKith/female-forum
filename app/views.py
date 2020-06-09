from django.shortcuts import render
from django.http import HttpResponse
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def pagination(object_list, request, per_page=20):
    page = request.GET.get('page')
    pages = Paginator(object_list, per_page)

    try:
        content = pages.page(page)
    except PageNotAnInteger:
        content = pages.page(1)
    except EmptyPage:
        content = pages.page(pages.num_pages)

    return content, page


tags = [f'tag{i}' for i in range(20)]
best_users = [f'user{i}' for i in range(20)]
answers = [
    {
        'id': i,
        'text': f'text#{i}',
        'author': f'author#{i}',
        'rate': random.randint(0, 20) - random.randint(0, 20)
    }
    for i in range(1, random.randint(10, 30))
]

questions = [
    {
        'id': i,
        'title': f'question #{i}',
        'text': f'text #{i}',
        'tags': random.choices(tags, k=random.randint(1, 3)),
        'author': f'author#{i}',
        'answers': answers,
        'num_answers': len(answers),
        'rate': random.randint(0, 20) - random.randint(0, 20)
    }
    for i in range(200)
]


def main(request):
    content, page = pagination(questions, request)
    return render(request, 'index.html', {
        'title': 'new questions',
        'page': page,
        'questions': content,
        'tags': tags,
        'best_users': best_users,
    })


def best_questions(request):
    content, page = pagination(sorted(questions, key=lambda x: x['likes'] - x['dislikes']), request)
    return render(request, 'index.html', {
        'title': 'best questions',
        'page': page,
        'questions': content,
        'tags': tags,
        'best_users': best_users,
    })


def tag_questions(request, cur_tag):
    content, page = pagination(list(filter(lambda x: cur_tag in x['tags'], questions)), request)
    return render(request, 'index.html', {
        'title': f'question about {cur_tag}',
        'page': page,
        'questions': content,
        'tags': tags,
        'best_users': best_users,
    })


def question(request, qid):
    content, page = pagination(questions[qid]['answers'], request, per_page=5)
    return render(request, 'question.html', {
        'tags': tags,
        'best_users': best_users,
        'question': questions[qid],
        'answers': content,
        'page': page
    })


def login(request):
    return render(request, 'signin.html', {
        'tags': tags,
        'best_users': best_users,
    })


def signup(request):
    return render(request, 'signup.html', {
        'tags': tags,
        'best_users': best_users,
    })


def ask(request):
    return render(request, 'ask.html', {
        'tags': tags,
        'best_users': best_users,
    })
