from django import forms


class ProductForm(forms.Form):
    title = forms.CharField(max_length=255)
    body_html = forms.CharField(widget=forms.Textarea)
    vendor = forms.CharField(max_length=100)
    product_type = forms.CharField(max_length=50)
    status = forms.CharField(max_length=20)
