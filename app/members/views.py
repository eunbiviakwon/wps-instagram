from django.contrib.auth import login, get_user_model, logout
from django.shortcuts import render, redirect

# 장고 기본유저나 Custom유저모델 중, 사용중인 User모델을 가져옴
from .forms import LoginForm, SignupForm

User = get_user_model()


def login_view(request):
    """
    Template: templates/members/login.html
        POST요청을 처리하는 form
        내부에는 input 2개를 가지며, 각각 username, password로 name을 가짐
    URL: /members/login/  (members.urls를 사용, config.urls에 include하여 사용)
            name: members:login (url namespace를 사용)
    POST요청시, 예제를 보고 적절히 로그인 처리한 후, index로 돌아갈 수 있도록 한다
    로그인에 실패하면 다시 로그인페이지로 이동
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return redirect('posts:post-list')
    else:
        form = LoginForm()

    context = {
        'form': form,
    }
    return render(request, 'members/login.html', context)


def signup_view(request):
    """
    ! config.views.index 삭제
    Template: index.html을 복사해서
              /members/signup.html
    URL:  /
    Form: members.forms.SignupForm
    생성에 성공하면 로그인 처리 후 (위의 login_view를 참조) posts:post-list로 redirect처리
    :return:
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('posts:post-list')
    else:
        form = SignupForm()

    context = {
        'form': form,
    }
    return render(request, 'members/signup.html', context)


def logout_view(request):
    """
    GET요청으로 처리함
    요청에 있는 사용자를 logout처리
    django.contrib.auth.logout함수를 사용한다
    URL: /members/logout/
    Template: 없음
    :param request:
    :return:
    """
    logout(request)
    return redirect('members:login')