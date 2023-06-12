from django import forms 
from django.conf import settings

from .models import CustomUser, Experience



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username',]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.' )
        return cd['password2']
    
class UserProfileEdit(forms.ModelForm):
    birth_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=False)
    class Meta:
        model = CustomUser
        exclude = ['is_staff', 'is_active', 'date_joined', 'is_deleted', 'password']

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = CustomUser.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            return forms.ValidationError("Email already in use")
        return data
    

class UserExperienceForm(forms.ModelForm):
    birth_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=False)
    class Meta:
        model = Experience
        exclude = ['user', 'date_created',]
