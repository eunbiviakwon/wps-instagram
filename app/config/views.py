from django.shortcuts import render, redirect


def index(request):
    """
    settings.TEMPLATES의 DIRS에
        instagram/app/templates 경로를 추가
    Template: templates/index.html
        <h1>Index!</h1>
    URL:      '/', name='index'
    base.html추가
        상단에 {% load static %}
        정적파일 불러올 때 {% static '경로' %}로 불러옴
    index.html과 login.html이 base.html을 extends하도록 함
    """
    if request.user.is_authenticated:
        return redirect('posts:post-list')
    return render(request, 'index.html')