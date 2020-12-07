from django import forms

# from grocerysite.grocerysite import settings


class Loginform(forms.Form):
  username= forms.CharField(max_length= 25,label="Username")
  password= forms.CharField(max_length= 30, label='Password', widget=forms.PasswordInput)


