from django import forms

# from grocerysite.grocerysite import settings


class Loginform(forms.Form):
  username= forms.CharField(max_length= 25,label="Username")
  password= forms.CharField(max_length= 30, label='Password', widget=forms.PasswordInput)


class Registerform(forms.Form):
  username= forms.CharField(max_length=25,label="Username")
  password= forms.CharField(max_length=30, label="Password", widget=forms.PasswordInput)
  address= forms.CharField(max_length=90, label="Address")
  phone= forms.CharField(max_length=14, label="Phone Number")

