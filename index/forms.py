from django import forms

class LoadForm(forms.Form):

    url = forms.URLField(max_length = 255,widget=forms.URLInput(attrs={'class' : 'form-control'}))
