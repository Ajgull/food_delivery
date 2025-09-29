from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField

from core import consts
from core.models import Profile


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}), help_text='write your passeord'
    )
    password2 = forms.CharField(
        label='Repeat Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
        help_text='repeat your password',
    )
    role = forms.ChoiceField(choices=consts.CHOISES, label='Role', help_text='choose your role')
    phone = PhoneNumberField()
    email = forms.EmailField(
        label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}), help_text='write your email'
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )

    def clean(self) -> dict:
        cd = self.cleaned_data
        password1 = cd.get('password1')
        password2 = cd.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return cd

    def save(self, commit: bool = True) -> User:
        user = super().save(commit)
        user.username = user.email
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                first_name=self.cleaned_data.get('first_name'),
                second_name=self.cleaned_data.get('last_name'),
                email=self.cleaned_data.get('email'),
                phone=self.cleaned_data.get('phone'),
                role=self.cleaned_data['role'],
            )
        return user


class UserLoginForm(forms.ModelForm):
    username = forms.CharField(
        label='Username', widget=forms.TextInput(attrs={'class': 'form-input'}), help_text='write unique username'
    )
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}), help_text='write your passeord'
    )

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self) -> dict:
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Invalid username or password.')

        return cleaned_data
