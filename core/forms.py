from django import forms
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
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                first_name=self.cleaned_data.get('first_name'),
                second_name=self.cleaned_data.get('second_name'),
                email=self.cleaned_data.get('email'),
                phone=self.cleaned_data.get('phone'),
                role=self.cleaned_data['role'],
            )

        return user
