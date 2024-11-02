from django import forms
from polls.models import AdvUser

class ChangeUserInfoForm(forms.ModelForm):
   email = forms.EmailField(required=True, label='Адрес электронной почты')
   avatar = forms.ImageField(required=False, label='Аватар', widget=forms.FileInput)

   class Meta:
       model = AdvUser
       fields = ('username', 'email', 'avatar')



