from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django import forms

from  .models import Account


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=200, help_text='Required') 

	class Meta(UserCreationForm.Meta):
		model = Account
		fields = ('email', 'password1', 'password2')

	def __init__(self, *args, **kwargs) -> None:
		super(RegistrationForm, self).__init__(*args, **kwargs)
		self.fields['email'].widget.attrs.update({'class':'form-control','placeholder':'Email'})
		self.fields['password1'].widget.attrs.update({'class':'form-control','placeholder':'Password'})
		self.fields['password2'].widget.attrs.update({'class':'form-control','placeholder':'Confirm Password'})


class LoginUserForm(AuthenticationForm):
	email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))

	class Meta:
		model = Account
		fields = ('email', 'password')

	def __init__(self, *args, **kwargs):
		super(LoginUserForm, self).__init__(*args, **kwargs)
		self.fields.pop('username')
		self.fields['email'].widget.attrs.update({'class':'form-control','placeholder':'Email'})
		self.fields['password'].widget.attrs.update({'class':'form-control','placeholder':'Password'})

