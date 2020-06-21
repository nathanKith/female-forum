from django.contrib import auth
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.models import Question, Answer, Profile, Tag, LikeAnswer, LikeQuestion
from app.forms import LoginForm, UserForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect


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
    q = get_object_or_404(Question, pk=qid)
    content, page = pagination(
        Answer.objects.question_answers(q),
        request,
        per_page=5,
    )
    return render(request, 'question.html', {
        'question': q,
        'answers': content,
        'page': page,
        **tags_and_users,
    })


def login(request):
    if request.method == 'POST':
        prev = request.GET.get('next', '')
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(prev)

            return render(request, 'signin.html', {
                'is_wrong': True,
                'error': 'Incorrect login or password',
                **tags_and_users,
            })

        return render(request, 'signin.html', {
            'is_wrong': True,
            'error': 'Incorrect login or password',
            **tags_and_users,
        })

    return render(request, 'signin.html', {
        'is_wrong': False,
        **tags_and_users,
    })


def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            auth_data = {
                'username': user.username,
                'password': user_form.cleaned_data['password1'],
            }
            u = auth.authenticate(request, **auth_data)
            if u is not None:
                auth.login(request, user)
                return redirect('/')

            return render(request, 'signup.html', {
                'form': user_form,
                **tags_and_users
            })

        return render(request, 'signup.html', {
            'form': user_form,
            **tags_and_users
        })
    return render(request, 'signup.html', tags_and_users)


@login_required
def ask(request):
    return render(request, 'ask.html', tags_and_users)


def logout(request):
    auth.logout(request)
    return redirect('/login')
