from django import forms
from users.models import User


class UserModelForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите имя'}),
        label='Имя',
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите фамилию'}),
        label='Фамилия'
    )
    job = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите професию'}),
        label='Профессия',
        required=False,
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'job')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-2 text-grey'
