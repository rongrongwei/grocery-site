from django import forms

from grocerysite.grocerysite import settings


class Loginform(forms.Form):
  username= forms.CharField(max_length= 25,label="Enter username")
  password= forms.CharField(max_length= 30, label='Password', widget=forms.PasswordInput)

class shoppingCart(object):
  def __init__(self, request):
    self.session = request.session
    cart = self.session.get(settings.CART_SESSION_ID)
    #save an empty cart in the session
    if not cart:
      cart = self.session[settings.CART_SESSION_ID] = {}
    self.cart = cart
