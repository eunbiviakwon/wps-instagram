from django.shortcuts import render


def index(request):
    return render(request, 'index.html')
    """
    settings.TEMPLATES의 DIRS에
        instagram/app/templates 경로를 추가
    Template: templates/index.html
        <h1>Index!</h1>
    URL:      '/', name='index'

    base.html추가
    상단에 {%load static '경로'%}로 불러옴

    index.html과 login.html이 base.html을 extend하도록 함
    return render(request, 'index.html')함
    """
