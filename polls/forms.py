from django import forms
from polls.models import AdvUser
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from .models import Question,Choice
from .models import user_registrated

class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    avatar = forms.ImageField(required=False, label='Аватар', widget=forms.FileInput)

    class Meta:  
        model = AdvUser  
        fields = ('username', 'email', 'avatar') 

class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль',
                                 widget=forms.PasswordInput,
                                 help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)',
                                 widget=forms.PasswordInput,
                                 help_text='Повторите тот же самый пароль еще раз')

    class Meta:
        model = AdvUser  
        fields = ('username', 'email', 'password1', 'password2') 
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
        user.is_active = False  
        user.is_activated = False
        if commit:
            user.save()
        user_registrated.send(sender=self.__class__, instance=user) 
        return user



class CreatePollForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'image']
        widgets = {
            'question_text': forms.TextInput(attrs={'placeholder': 'Введите текст вопроса'}),
        }


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
        widgets = {
            'choice_text': forms.TextInput(attrs={'placeholder': 'Введите вариант ответа'}),
        }
ChoiceFormSet = modelformset_factory(Choice, form=ChoiceForm, extra=3)