import re

from django import forms

from main.models import User, Trip, Transport


class AuthForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Электронная почта',
        'class': 'form-floating'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Пароль',
        'class': 'form-floating'
    }))


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'email')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Эта почта уже зарегистрирована')
        return email

    def clean_password2(self):
        reg = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{6,20}$')
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            self.add_error('password1', 'Пароли не совпадают')
        if not reg.match(password1):
            self.add_error('password1', 'Пароль должен содержать цифру, по одной букве латинского алфавита в верхнем и '
                                        'нижнем регистре и не менее 6 символов')
        return password1


class FindForm(forms.ModelForm):
    city = forms.CharField(max_length=50, required=False)
    date = forms.DateField(required=False)
    transport = forms.ModelMultipleChoiceField(queryset=Transport.objects.all(),
                                               required=False)

    class Meta:
        model = Trip
        fields = ('country',)


class ImageForm(forms.Form):
    avatar = forms.ImageField()


class ResetEmailForm(forms.Form):
    email = forms.EmailField()


class ResetPasswordForm(forms.Form):
    password = forms.CharField()
