from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '아이디 넣어주세요',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'placeholder': '비밀번호 넣어주세요',
            }
        )
    )


class SignupForm(forms.Form):
    def save(self):
        """
        Form으로 전달받은 데이터를 사용해서
        새로운 User를 생성하고 리턴
        username과 email검증로직도 이 안에 넣기!
        """
        pass