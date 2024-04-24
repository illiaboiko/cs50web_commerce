from django import forms
from .models import Listing, Comment, Bid, Category


class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title",
            "description",
            "start_time",
            "end_time",
            # "current_price",
            "categories",
            "image_url",
        ]
        
        widgets = {
            "start_time": forms.TextInput(attrs={
                "class": "datepicker"
            }),
            "end_time": forms.TextInput(attrs={
                "class": "datepicker"
            })
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category"]

# example of handling styling of model forms:
# class UserInfoForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['name', 'email']
#         widgets = {
#             'name': TextInput(attrs={
#                 'class': "form-control",
#                 'style': 'max-width: 300px;',
#                 'placeholder': 'Name'
#                 }),
#             'email': EmailInput(attrs={
#                 'class': "form-control", 
#                 'style': 'max-width: 300px;',
#                 'placeholder': 'Email'
#                 })
#         }