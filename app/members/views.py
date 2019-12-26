from django.contrib.auth import authenticate, login
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
            return redirect('index')
        else:
            return redirect('members:login')
    return render(request, 'members/login.html')