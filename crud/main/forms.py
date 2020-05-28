from django import forms
from .models import *
def hey(i):
	print(i)
	return(i)
class student_form(forms.Form):
	name=forms.CharField()