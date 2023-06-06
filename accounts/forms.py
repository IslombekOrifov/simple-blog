from django import forms 
from .models import CustomUser


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
    
class UserProfile(forms.ModelForm):
    class Meta:
        model = CustomUser
        exclude = ['is_staff', 'is_active', 'date_joined', 'is_deleted']
