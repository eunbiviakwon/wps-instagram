from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def login_view(request):
    """
    Template: templates/members/login.html
        POST요청을 처리하는 form
        내부에는 input 2개를 가지며, 각각 username, password로 name을 가짐
    URL: /members/login/  (members.urls를 사용, config.urls에 include하여 사용)
            name: members:login (url namespace를 사용)
    POST요청시, 예제를 보고 적절히 로그인 처리한 후, index로 돌아갈 수 있도록 한다
    로그인에 실패하면 다시 로그인페이지로 이동
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print('username:', username)
        print('password:', password)
        user = authenticate(request, username=username, password=password)
        print('user:', user)
        if user:
            login(request, user)
            return redirect('posts:post-list')
        else:
            return redirect('members:login')
    return render(request, 'members/login.html')


def signup_view(request):
    """
    Template: index.html을 그대로 사용
        action만 이쪽으로
    URL: /members/signup/
    User에 name필드를 추가
        email
        username
        name
        password
    를 전달받아, 새로운 User를 생성한다
    생성시, User.objects.create_user() 메서드를 사용한다
    이미 존재하는 username또는 email을 입력한 경우,
    "이미 사용중인 username/email입니다" 라는 메시지를 HttpResponse로 돌려준다
    생성에 성공하면 로그인 처리 후 (위의 login_view를 참조) posts:post-list로 redirect처리
    :param request:
    :return:
    """
    email = request.POST['email']
    username = request.POST['username']
    name = request.POST['name']
    password = request.POST['password']

    if User.objects.filter(username=username).exists():
        return HttpResponse('이미 사용중인 username입니다')
    if User.objects.filter(email=email).exists():
        return HttpResponse('이미 사용중인 email입니다')


    user = User.objects.create_user(
        username=username,
        email=email,
        name=name,
        password=password,
    )
    login(request, user)
    return redirect('posts:post-list')

def logout_view(request):

    """
    GET 요청으로 처리함
    요청에 있는 사용자를 logout 처리
    django.contrib.auth.logout 함수를 사용한다

    URL: /members/logout/
    Template: 없음

    :param request:
    :return:
    """
    logout(request)
    return redirect('members:login')