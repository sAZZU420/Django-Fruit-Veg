from .models import Account
from django import forms


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
        'id': 'password'
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
        'id': 'pass'
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg'
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg'
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-lg'
    }))

    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password',]

    def clean(self):
        clean_data = super(RegistrationForm, self).clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Password does not match'
            )
