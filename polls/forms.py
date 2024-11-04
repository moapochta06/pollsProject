from django import forms
from polls.models import AdvUser
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import user_registrated

class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    avatar = forms.ImageField(required=False, label='Аватар', widget=forms.FileInput)

    class Meta:  # Ensure this is properly indented
        model = AdvUser  # Correctly specify the model here
        fields = ('username', 'email', 'avatar')  # Specify the fields you want to include

class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль',
                                 widget=forms.PasswordInput,
                                 help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)',
                                 widget=forms.PasswordInput,
                                 help_text='Повторите тот же самый пароль еще раз')

    class Meta:
        model = AdvUser  # Correctly specify the model here
        fields = ('username', 'email', 'password1', 'password2')  # Include password fields

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError({'password2': 'Введенные пароли не совпадают'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False  # Assuming you want to deactivate until activation
        user.is_activated = False
        if commit:
            user.save()
        user_registrated.send(sender=self.__class__, instance=user)  # Correct signal sending
        return user





