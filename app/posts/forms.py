from django import forms


class PostCreateForm(forms.Form):
    """
    이 Form에 들어갈 입력요소
    Imange(Field)
    Text
    """
    img = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True,
            }
        )
    )
    text = forms.CharField(max_length=500)

