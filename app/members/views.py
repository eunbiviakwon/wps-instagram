import requests
from django.contrib.auth import login, get_user_model, logout
from django.http import HttpResponse
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

    login_base_url = 'http://nid.naver.com/oauth2.0/authorize'
    login_params = {
        'response_type': 'code',
        'client_id': 'wJcJbLrIqZv3Nq83VgKZ',
        'redirect_uri': "http://localhost:8000/members/naver-login/",
        'state': 'RANDOM_STATE',
    }
    login_url = '{base}?{params}'.format(
        base=login_base_url,
        params='&'.join([f'{key}={value}' for key, value in login_params.items()])
    )
    print(login_url)

    context = {
        'form': form,
        'login_url': login_url,
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
            login(request, user)
            return redirect('/')
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


def naver_login(request):
    # GET parameter로 전달된 'code'값을 사용해서
    # 네이버 API의 PHP 샘플 코드를 보고
    # token_url을 생성
    # print(token_url)
    code = request.GET.get('code')
    state = request.GET.get('state')
    if not code or not state:
        return HttpResponse('code 또는 state가 전달되지 않았습니다.')

    token_base_url = 'https://nid.naver.com/oauth2.0/token'
    token_params = {
        'grant_type': 'authorization_code',
        'client_id': 'wJcJbLrIqZv3Nq83VgKZ',
        'client_secret':'hk2BMmOfeG',
        'code': code,
        'state': state,
        'redirectURI' : 'http://localhost:8000/members/naver-login/',
    }

    token_url = '{base}?{params}'.format(
        base=token_base_url,
        params='&'.join([f'{key}={value}' for key, value in token_params.items()])
    )
    response = requests.get(token_url)
    access_token = response.json()['access_token']
    print(access_token)

    me_url= 'https://openapi.naver.com/v1/nid/me'
    me_headers = {
        'Authorization': f'Bearer {access_token}',
    }
    me_response = requests.get(me_url, headers=me_headers)
    me_response_data = me_response.json()
    print(me_response_data)

    unique_id = me_response_data['response']['id']
    print(unique_id)

    # n_{unique_id} 의 username을 갖는 새로운 User를 생성
    # 생성한 유저를 login시킴
    # posts:post-list로 이동시킴
    naver_username = f'n_{unique_id}'
    if not User.objects.filter(username=naver_username).exists():
        user = User.objects.create_user(username=naver_username)
        login(request, user)
    return redirect('/')



    # token URL에
    # GET요청을 보내고 그 요청의 response를 받아와서
    # client_id = 'wJcJbLrIqZv3Nq83VgKZ'
    # redirect_uri = "http://localhost:8000/members/naver-login/"
    # client_secret = 'hk2BMmOfeG'
    # url = f'https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id="{client_id}"&client_secret="{client_secret}"&redirect_uri="{redirect_uri}'
    #
    # pass